#!/usr/bin/env python3
"""Plan or run the smallest configured validation set for changed paths."""

import argparse
import fnmatch
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MAP = ROOT / ".mamkin/validation-map.json"


def matches(path, pattern):
    return fnmatch.fnmatchcase(path, pattern)


def changed_paths(root):
    has_head = subprocess.run(
        ["git", "rev-parse", "--verify", "HEAD"],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    ).returncode == 0
    tracked_command = (
        ["git", "diff", "--name-only", "HEAD"]
        if has_head
        else ["git", "ls-files"]
    )
    tracked = subprocess.run(
        tracked_command,
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    return sorted(set(tracked + untracked))


def build_plan(config, paths):
    selected = {}
    for check_id in config.get("always", []):
        selected.setdefault(check_id, []).append("always")

    process_patterns = config.get("processOnlyPatterns", [])
    unknown_check = config.get("unknownPathCheck")
    for path in paths:
        matched_rule = False
        for rule in config.get("rules", []):
            if any(matches(path, pattern) for pattern in rule.get("patterns", [])):
                matched_rule = True
                for check_id in rule.get("checks", []):
                    selected.setdefault(check_id, []).append(path)
        if not matched_rule and not any(matches(path, pattern) for pattern in process_patterns):
            selected.setdefault(unknown_check, []).append(path)
    return selected


def validate_config(config):
    if config.get("schemaVersion") != 1:
        raise ValueError("validation map schemaVersion must be 1")
    checks = config.get("checks")
    if not isinstance(checks, dict) or not checks:
        raise ValueError("validation map checks must be a non-empty object")
    unknown_check = config.get("unknownPathCheck")
    if not isinstance(unknown_check, str) or not unknown_check:
        raise ValueError("validation map unknownPathCheck must name one check")
    referenced = set(config.get("always", []))
    referenced.add(unknown_check)
    for rule in config.get("rules", []):
        referenced.update(rule.get("checks", []))
    missing = sorted(check_id for check_id in referenced if check_id not in checks)
    if missing:
        raise ValueError(f"validation map references unknown checks: {missing}")
    for check_id, entry in checks.items():
        command = entry.get("command")
        if command is not None and (
            not isinstance(command, list)
            or not command
            or not all(isinstance(part, str) and part for part in command)
        ):
            raise ValueError(f"check {check_id} command must be null or a non-empty argv array")


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*", help="Changed paths; defaults to current Git changes")
    parser.add_argument("--map", dest="map_path", default=str(DEFAULT_MAP))
    parser.add_argument("--run", action="store_true", help="Run the selected checks")
    args = parser.parse_args(argv)

    map_path = Path(args.map_path)
    config = json.loads(map_path.read_text(encoding="utf-8"))
    try:
        validate_config(config)
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2

    paths = sorted(set(args.paths or changed_paths(ROOT)))
    plan = build_plan(config, paths)
    print("Changed paths:")
    for path in paths:
        print(f"- {path}")
    print("Selected checks:")

    missing_commands = []
    for check_id, reasons in plan.items():
        command = config["checks"][check_id].get("command")
        rendered = "UNCONFIGURED" if command is None else " ".join(command)
        print(f"- {check_id}: {rendered} ({', '.join(reasons)})")
        if command is None:
            missing_commands.append(check_id)

    if not args.run:
        return 0
    if missing_commands:
        print(
            f"ERROR: required checks are unconfigured: {sorted(missing_commands)}",
            file=sys.stderr,
        )
        return 2

    failed = []
    for check_id in plan:
        command = config["checks"][check_id]["command"]
        print(f"\nRunning {check_id}: {' '.join(command)}")
        result = subprocess.run(command, cwd=ROOT, check=False)
        if result.returncode:
            failed.append((check_id, result.returncode))
    if failed:
        for check_id, returncode in failed:
            print(f"ERROR: {check_id} exited {returncode}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
