#!/usr/bin/env python3
"""Review or safely apply allowlisted Mamkin process updates from a local clone."""

import argparse
import fnmatch
import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ".mamkin/process-manifest.json"
VERSION_PATH = ".mamkin/template-version.json"


def git(root, *args, check=True):
    return subprocess.run(
        ["git", *args],
        cwd=root,
        check=check,
        capture_output=True,
        text=True,
    )


def git_head(root):
    return git(root, "rev-parse", "HEAD").stdout.strip()


def git_clean(root):
    return not git(root, "status", "--porcelain").stdout.strip()


def git_file(root, commit, path):
    result = subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=root,
        check=False,
        capture_output=True,
    )
    if result.returncode:
        return None
    return result.stdout


def git_paths(root, commit):
    result = git(root, "ls-tree", "-r", "--name-only", commit, check=False)
    return set(result.stdout.splitlines()) if result.returncode == 0 else set()


def read_bytes(root, path):
    candidate = root / path
    if candidate.is_symlink():
        raise ValueError(f"refusing symlink: {candidate}")
    if not candidate.exists():
        return None
    if not candidate.is_file():
        raise ValueError(f"refusing non-regular file: {candidate}")
    return candidate.read_bytes()


def matches(path, patterns):
    return any(fnmatch.fnmatchcase(path, pattern) for pattern in patterns)


def classify(path, manifest):
    for name in ("neverSync", "projectOwned", "mixed", "templateOwned"):
        if matches(path, manifest.get(name, [])):
            return name
    return "unclassified"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate_manifest(manifest):
    if manifest.get("schemaVersion") != 1:
        raise ValueError("process manifest schemaVersion must be 1")
    for name in ("templateOwned", "mixed", "projectOwned", "neverSync"):
        values = manifest.get(name)
        if not isinstance(values, list) or not all(
            isinstance(value, str) and value and not value.startswith("/")
            for value in values
        ):
            raise ValueError(f"manifest {name} must be a list of relative patterns")


def inventory(root):
    return {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file() and ".git" not in path.relative_to(root).parts
    }


def plan_sync(source, target, manifest, baseline):
    source_paths = inventory(source)
    target_paths = inventory(target)
    base_paths = git_paths(source, baseline) if baseline else set()
    all_paths = sorted(source_paths | target_paths | base_paths)
    plan = []
    for path in all_paths:
        if path == VERSION_PATH:
            continue
        ownership = classify(path, manifest)
        if ownership not in {"templateOwned", "mixed", "projectOwned"}:
            continue
        ours = read_bytes(target, path)
        theirs = read_bytes(source, path)
        if ours == theirs:
            continue
        base = git_file(source, baseline, path) if baseline else None
        if ownership == "mixed":
            if baseline and theirs == base:
                action = "local-only"
            elif baseline and ours == base:
                action = "manual-update"
            else:
                action = "manual-merge"
        elif ownership == "projectOwned":
            action = "protected"
        elif baseline:
            if ours == base:
                action = "safe-update"
            elif theirs == base:
                action = "local-only"
            else:
                action = "conflict"
        else:
            action = "two-way-review"
        plan.append(
            {
                "path": path,
                "ownership": ownership,
                "action": action,
                "sourceState": "deleted" if theirs is None else "present",
            }
        )
    return plan


def valid_commit(root, commit):
    if not commit or commit == "TBD":
        return False
    return git(root, "cat-file", "-e", f"{commit}^{{commit}}", check=False).returncode == 0


def apply_entry(source, target, entry, prune):
    relative = entry["path"]
    source_path = source / relative
    target_path = target / relative
    if entry["sourceState"] == "deleted":
        if not prune:
            return "skipped-deletion"
        if target_path.is_symlink():
            raise ValueError(f"refusing to delete symlink: {target_path}")
        target_path.unlink()
        return "deleted"
    if source_path.is_symlink() or not source_path.is_file():
        raise ValueError(f"refusing non-regular source file: {source_path}")
    target_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_path, target_path)
    return "updated"


def render_report(
    source_head,
    target_head,
    source_clean,
    target_clean,
    metadata,
    baseline,
    plan,
    applied=None,
):
    print(f"Source commit: {source_head}")
    print(f"Source clean at review: {source_clean}")
    print(f"Target commit: {target_head}")
    print(f"Target clean at review: {target_clean}")
    print(f"Recorded template commit: {metadata.get('templateCommit', 'unknown')}")
    print(f"Recorded last sync commit: {metadata.get('lastProcessSyncCommit', 'unknown')}")
    print(f"Usable three-way baseline: {baseline or 'unknown'}")
    if not plan:
        print("No process differences found.")
        return
    print("Process differences:")
    for entry in plan:
        suffix = f" -> {applied[entry['path']]}" if applied and entry["path"] in applied else ""
        print(
            f"- {entry['path']}: {entry['ownership']} / {entry['action']} "
            f"/ source {entry['sourceState']}{suffix}"
        )


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, help="Verified local mamkin-builder clone")
    parser.add_argument("--target", default=str(ROOT), help="Copied project to inspect")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--expected-source-commit")
    parser.add_argument(
        "--accept-two-way",
        action="store_true",
        help="Allow template-owned updates after a reviewed first-sync comparison",
    )
    parser.add_argument(
        "--prune",
        action="store_true",
        help="Delete removed template-owned files when the plan marks them safe",
    )
    parser.add_argument(
        "--acknowledge-mixed",
        action="append",
        default=[],
        metavar="PATH",
        help="Confirm one reviewed mixed file was manually merged or intentionally preserved",
    )
    args = parser.parse_args(argv)

    source = Path(args.source).resolve()
    target = Path(args.target).resolve()
    if source == target:
        print("ERROR: source and target must be different repositories", file=sys.stderr)
        return 2

    try:
        manifest = load_json(target / MANIFEST_PATH)
        validate_manifest(manifest)
        metadata = load_json(target / VERSION_PATH)
        source_head = git_head(source)
        target_head = git_head(target)
        source_clean = git_clean(source)
        target_clean = git_clean(target)
    except (FileNotFoundError, ValueError, json.JSONDecodeError, subprocess.CalledProcessError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2

    baseline_value = metadata.get("lastProcessSyncCommit")
    if baseline_value == "TBD":
        baseline_value = metadata.get("templateCommit")
    baseline = baseline_value if valid_commit(source, baseline_value) else None

    try:
        plan = plan_sync(source, target, manifest, baseline)
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2

    if not args.apply:
        render_report(
            source_head,
            target_head,
            source_clean,
            target_clean,
            metadata,
            baseline,
            plan,
        )
        print("Mode: review only; no files changed.")
        return 0

    if args.expected_source_commit != source_head:
        print(
            "ERROR: --expected-source-commit must match the reviewed source HEAD",
            file=sys.stderr,
        )
        return 2
    if git_head(source) != source_head:
        print("ERROR: source HEAD moved after review planning", file=sys.stderr)
        return 2
    if git_head(target) != target_head:
        print("ERROR: target HEAD moved after review planning", file=sys.stderr)
        return 2
    if not source_clean or not git_clean(source):
        print("ERROR: source repository is dirty", file=sys.stderr)
        return 2
    if not target_clean or not git_clean(target):
        print("ERROR: target repository is dirty", file=sys.stderr)
        return 2

    blocking = []
    applicable = []
    acknowledged_mixed = set(args.acknowledge_mixed)
    reported_mixed = {
        entry["path"] for entry in plan if entry["ownership"] == "mixed"
    }
    unknown_acknowledgements = acknowledged_mixed - reported_mixed
    if unknown_acknowledgements:
        print(
            "ERROR: acknowledged mixed paths are not reported mixed differences: "
            f"{sorted(unknown_acknowledgements)}",
            file=sys.stderr,
        )
        return 2
    for entry in plan:
        if entry["ownership"] != "templateOwned":
            if (
                entry["ownership"] == "mixed"
                and entry["action"] != "local-only"
                and (
                    entry["action"] == "manual-update"
                    or entry["path"] not in acknowledged_mixed
                )
            ):
                blocking.append(entry)
            continue
        if entry["action"] == "safe-update":
            applicable.append(entry)
        elif entry["action"] == "two-way-review" and args.accept_two_way:
            applicable.append(entry)
        elif entry["action"] not in {"local-only"}:
            blocking.append(entry)

    for entry in applicable:
        if entry["sourceState"] == "deleted" and not args.prune:
            blocking.append(entry)
    if blocking:
        render_report(
            source_head,
            target_head,
            source_clean,
            target_clean,
            metadata,
            baseline,
            plan,
        )
        print("Apply blocked: manual or explicitly pruned items remain.", file=sys.stderr)
        return 1

    applied = {}
    try:
        for entry in applicable:
            result = apply_entry(source, target, entry, args.prune)
            applied[entry["path"]] = result
    except (OSError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2

    updated_metadata = dict(metadata)
    updated_metadata["lastProcessSyncCommit"] = source_head
    (target / VERSION_PATH).write_text(
        json.dumps(updated_metadata, indent=2) + "\n", encoding="utf-8"
    )
    applied[VERSION_PATH] = "metadata-updated"

    render_report(
        source_head,
        target_head,
        source_clean,
        target_clean,
        metadata,
        baseline,
        plan,
        applied,
    )
    print("Apply complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
