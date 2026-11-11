#!/usr/bin/env python3
"""Execute the frozen Stage-2 sequence; no product scheduler is installed."""

import argparse
import hashlib
import json
import subprocess
import time
from pathlib import Path

import cases
import checks


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if not args.output.is_absolute() or args.output.exists():
        parser.error("--output must be a new absolute disposable directory")
    args.output.mkdir()
    roots = {}
    commit = subprocess.check_output(["git", "-C", str(checks.REPO), "rev-parse", "HEAD"], text=True).strip()
    sources = [checks.HERE / name for name in ("cases.py", "checks.py", "run.py")]
    sources += [checks.REPO / ".agents/skills" / name / "SKILL.md" for name in checks.SKILLS]
    hashes = {str(p.relative_to(checks.REPO)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    for case in cases.CASES:
        cid = case["id"]
        if case["group"] not in roots:
            root = args.output / case["group"]
            checks.prepare(root, case)
            roots[case["group"]] = root
        root = roots[case["group"]]
        before = checks.snapshot(root)
        save(args.output / f"{cid}-before.json", before)
        argv = ["codex", "--no-daemon", "-a", "on-request", "exec", "--ephemeral", "--json",
                "--model", "gpt-6.1-sol", "-c", 'model_reasoning_effort="high"',
                "--sandbox", "workspace-write", "--skip-git-repo-check", "--cd", str(root),
                "--output-last-message", str(args.output / f"{cid}-final.txt"), "-"]
        start = time.monotonic()
        with (args.output / f"{cid}-events.jsonl").open("w") as out, (args.output / f"{cid}-stderr.txt").open("w") as err:
            try:
                proc = subprocess.run(argv, input=case["prompt"], text=True, stdout=out, stderr=err, timeout=240)
                launch = {"exitCode": proc.returncode, "timedOut": False}
            except subprocess.TimeoutExpired:
                launch = {"exitCode": None, "timedOut": True}
        elapsed = round(time.monotonic() - start, 3)
        events = []
        for line in (args.output / f"{cid}-events.jsonl").read_text().splitlines():
            try:
                events.append(json.loads(line))
            except ValueError:
                pass
        turns = [e for e in events if e.get("type") == "turn.completed"]
        threads = [e.get("thread_id", "") for e in events if e.get("type") == "thread.started"]
        commands = [e["item"] for e in events if e.get("type") == "item.completed" and e.get("item", {}).get("type") == "command_execution"]
        changes = [e["item"] for e in events if e.get("type") == "item.completed" and e.get("item", {}).get("type") == "file_change"]
        result = {"case": cid, "group": case["group"], "criteriaCommit": commit, "sourceHashes": hashes,
                  "launch": {**launch, "argv": argv, "elapsedSeconds": elapsed, "completedTurns": len(turns),
                             "threadIdentityHashes": [hashlib.sha256(t.encode()).hexdigest() for t in threads],
                             "reportedUsage": [e.get("usage") for e in turns], "cost": None},
                  "deterministic": checks.check(case, root, before),
                  "commandEvidence": [{"command": c.get("command"), "exitCode": c.get("exit_code"), "output": c.get("aggregated_output", "")[-1800:]} for c in commands],
                  "fileChangeEvidence": changes,
                  "behavioral": {"pass": None, "criteria": case["criteria"]}}
        save(args.output / f"{cid}-after.json", checks.snapshot(root))
        save(args.output / f"{cid}-result.json", result)
        print(json.dumps({"case": cid, "exitCode": launch["exitCode"], "completedTurns": len(turns),
                          "deterministicPass": result["deterministic"]["pass"], "elapsedSeconds": elapsed}), flush=True)
        if launch["exitCode"] != 0 or not turns or not result["deterministic"]["pass"]:
            raise SystemExit("Stopped: preserve evidence and inspect before continuing.")


if __name__ == "__main__":
    main()
