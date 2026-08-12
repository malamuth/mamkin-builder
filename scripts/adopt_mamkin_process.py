#!/usr/bin/env python3
"""Review or seed Mamkin process files into an existing Git repository."""

import argparse
import copy
import fnmatch
import hashlib
import json
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


def is_git_repo(root):
    return git(root, "rev-parse", "--show-toplevel", check=False).returncode == 0


def git_head(root):
    return git(root, "rev-parse", "HEAD").stdout.strip()


def git_root(root):
    return Path(git(root, "rev-parse", "--show-toplevel").stdout.strip()).resolve()


def git_clean(root):
    return not git(root, "status", "--porcelain").stdout.strip()


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def matches(path, patterns):
    return any(fnmatch.fnmatchcase(path, pattern) for pattern in patterns)


def classify(path, manifest):
    for name in ("neverSync", "projectOwned", "mixed", "templateOwned"):
        if matches(path, manifest.get(name, [])):
            return name
    return "unclassified"


def validate_manifest(manifest):
    if manifest.get("schemaVersion") != 1:
        raise ValueError("process manifest schemaVersion must be 1")
    for name in ("templateOwned", "mixed", "projectOwned", "neverSync"):
        values = manifest.get(name)
        if not isinstance(values, list) or not all(
            isinstance(value, str)
            and value
            and not value.startswith("/")
            and ".." not in Path(value).parts
            for value in values
        ):
            raise ValueError(f"manifest {name} must contain safe relative patterns")


def inventory(root):
    paths = set()
    for candidate in root.rglob("*"):
        relative = candidate.relative_to(root)
        if ".git" in relative.parts:
            continue
        if candidate.is_file() or candidate.is_symlink():
            paths.add(relative.as_posix())
    return paths


def tracked_paths(root, commit):
    result = git(root, "ls-tree", "-r", "--name-only", commit)
    return set(result.stdout.splitlines())


def classify_repository(target):
    target_paths = inventory(target)
    version_path = target / VERSION_PATH
    manifest_path = target / MANIFEST_PATH
    if version_path.exists():
        try:
            metadata = load_json(version_path)
        except (json.JSONDecodeError, OSError):
            return "partial-adoption"
        if metadata.get("initializedProject") is True and manifest_path.is_file():
            return "already-initialized"
        return "partial-adoption"
    mamkin_markers = (
        manifest_path.exists()
        or any(path.startswith(".agents/skills/mamkin-") for path in target_paths)
        or "docs/process/agent-orchestration.md" in target_paths
    )
    if mamkin_markers:
        return "partial-adoption"
    if not target_paths:
        return "new-or-empty"
    return "brownfield"


def plan_adoption(source, target, manifest, source_head=None):
    source_head = source_head or git_head(source)
    source_paths = tracked_paths(source, source_head)
    entries = []
    for path in sorted(source_paths):
        if path in {MANIFEST_PATH, VERSION_PATH}:
            continue
        ownership = classify(path, manifest)
        if ownership == "templateOwned":
            source_path = source / path
            target_path = target / path
            if source_path.is_symlink() or not source_path.is_file():
                action = "blocked-source"
            elif target_path.exists() or target_path.is_symlink():
                action = "protect-existing"
            else:
                action = "seed"
        elif ownership == "mixed":
            target_path = target / path
            action = (
                "manual-merge"
                if target_path.exists() or target_path.is_symlink()
                else "manual-create"
            )
        elif ownership == "projectOwned":
            action = "create-project-context"
        else:
            continue
        entries.append(
            {
                "path": path,
                "ownership": ownership,
                "action": action,
            }
        )
    return entries


def plan_digest(source_head, target_head, classification, source_clean, target_clean, entries):
    payload = {
        "schemaVersion": 1,
        "sourceHead": source_head,
        "targetHead": target_head,
        "classification": classification,
        "sourceClean": source_clean,
        "targetClean": target_clean,
        "entries": entries,
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def target_manifest(source_manifest, entries):
    result = copy.deepcopy(source_manifest)
    protected = result.setdefault("projectOwned", [])
    for entry in entries:
        if entry["action"] == "protect-existing" and entry["path"] not in protected:
            protected.append(entry["path"])
    return result


def target_metadata(source_metadata, source_head, target_head):
    return {
        "schemaVersion": 1,
        "templateName": source_metadata.get("templateName", "mamkin-builder"),
        "templateRepo": source_metadata.get("templateRepo", "TBD"),
        "templateCommit": source_head,
        "lastProcessSyncCommit": source_head,
        "initializedProject": True,
        "adoptionMode": "brownfield",
        "adoptedFromProjectCommit": target_head,
        "ownershipManifest": MANIFEST_PATH,
        "notes": [
            "Mamkin was adopted into an existing repository at the recorded project commit.",
            "Pre-existing target collisions are protected by the project ownership manifest.",
            "Product files, Git state, secrets, remotes, and external resources remain project-owned.",
        ],
    }


def ensure_regular_source(source, relative):
    candidate = source / relative
    if candidate.is_symlink() or not candidate.is_file():
        raise ValueError(f"refusing non-regular source file: {candidate}")
    return candidate


def ensure_absent_safe_target(target, relative):
    candidate = target / relative
    if candidate.exists() or candidate.is_symlink():
        raise ValueError(f"refusing existing target path: {candidate}")
    current = target
    for part in Path(relative).parts[:-1]:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"refusing symlinked target parent: {current}")
        if current.exists() and not current.is_dir():
            raise ValueError(f"refusing non-directory target parent: {current}")
    return candidate


def write_new_file(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(content)


def remove_created(target, created):
    for path in reversed(created):
        try:
            path.unlink()
        except FileNotFoundError:
            pass
    candidate_dirs = set()
    for path in created:
        for parent in path.parents:
            if parent == target:
                break
            candidate_dirs.add(parent)
    candidate_dirs = sorted(candidate_dirs, key=lambda path: len(path.parts), reverse=True)
    for directory in candidate_dirs:
        try:
            directory.rmdir()
        except OSError:
            pass


def apply_adoption(source, target, source_manifest, source_metadata, entries, source_head, target_head):
    seed_entries = [entry for entry in entries if entry["action"] == "seed"]
    prepared = []
    for entry in seed_entries:
        source_path = ensure_regular_source(source, entry["path"])
        target_path = ensure_absent_safe_target(target, entry["path"])
        prepared.append((target_path, source_path.read_bytes()))

    manifest_path = ensure_absent_safe_target(target, MANIFEST_PATH)
    version_path = ensure_absent_safe_target(target, VERSION_PATH)
    manifest_bytes = (json.dumps(target_manifest(source_manifest, entries), indent=2) + "\n").encode("utf-8")
    metadata_bytes = (
        json.dumps(target_metadata(source_metadata, source_head, target_head), indent=2) + "\n"
    ).encode("utf-8")

    created = []
    try:
        for target_path, content in prepared:
            write_new_file(target_path, content)
            created.append(target_path)
        write_new_file(manifest_path, manifest_bytes)
        created.append(manifest_path)
        write_new_file(version_path, metadata_bytes)
        created.append(version_path)
    except (OSError, ValueError):
        remove_created(target, created)
        raise
    return [path.relative_to(target).as_posix() for path in created]


def render_report(state, entries, digest, applied=None):
    print(f"Status: {state['status']}")
    print(f"Repository classification: {state['classification']}")
    print(f"Source commit: {state['sourceHead']}")
    print(f"Source clean at review: {state['sourceClean']}")
    print(f"Target commit: {state['targetHead'] or 'unavailable'}")
    print(f"Target clean at review: {state['targetClean']}")
    print(f"Plan digest: {digest or 'not-applicable'}")
    if entries:
        print("Adoption plan:")
        for entry in entries:
            print(f"- {entry['path']}: {entry['ownership']} / {entry['action']}")
    if applied is not None:
        print("Applied files:")
        for path in applied:
            print(f"- {path}")
        manual = [entry["path"] for entry in entries if entry["action"].startswith("manual-")]
        project_context = [
            entry["path"] for entry in entries if entry["action"] == "create-project-context"
        ]
        print(f"Manual reconciliation remaining: {len(manual)}")
        print(f"Project-context files remaining: {len(project_context)}")


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, help="Verified local mamkin-builder checkout")
    parser.add_argument("--target", default=str(ROOT), help="Existing project to inspect")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--expected-source-commit")
    parser.add_argument("--expected-target-commit")
    parser.add_argument("--expected-plan-digest")
    args = parser.parse_args(argv)

    source = Path(args.source).resolve()
    target = Path(args.target).resolve()
    if source == target:
        print("ERROR: source and target must be different repositories", file=sys.stderr)
        return 2
    if not source.is_dir() or not target.is_dir():
        print("ERROR: source and target must be existing directories", file=sys.stderr)
        return 2
    if not is_git_repo(source):
        print("ERROR: source must be a Git repository", file=sys.stderr)
        return 2

    try:
        source_head = git_head(source)
        source_tracked = tracked_paths(source, source_head)
        if MANIFEST_PATH not in source_tracked or VERSION_PATH not in source_tracked:
            raise ValueError("source manifest and version metadata must be tracked at source HEAD")
        source_manifest = load_json(source / MANIFEST_PATH)
        validate_manifest(source_manifest)
        source_metadata = load_json(source / VERSION_PATH)
        source_clean = git_clean(source)
        target_is_git = is_git_repo(target)
        target_is_root = target_is_git and git_root(target) == target
        target_head = git_head(target) if target_is_git else None
        target_clean = git_clean(target) if target_is_git else False
        classification = classify_repository(target)
        entries = plan_adoption(source, target, source_manifest, source_head)
    except (FileNotFoundError, ValueError, json.JSONDecodeError, subprocess.CalledProcessError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2

    unsafe_source = any(entry["action"] == "blocked-source" for entry in entries)
    eligible = (
        classification == "brownfield"
        and target_is_git
        and target_is_root
        and not unsafe_source
    )
    digest = plan_digest(
        source_head,
        target_head,
        classification,
        source_clean,
        target_clean,
        entries,
    )
    if classification == "already-initialized":
        status = "Already initialized - use template sync"
    elif classification == "new-or-empty":
        status = "Not eligible - use init"
    elif classification == "partial-adoption":
        status = "Blocked - partial adoption requires recovery review"
    elif not target_is_git:
        status = "Blocked - Git baseline required"
    elif not target_is_root:
        status = "Blocked - target must be the Git root"
    elif unsafe_source:
        status = "Blocked - source contains a non-regular process path"
    elif target_clean and source_clean:
        status = "Ready for approval"
    else:
        status = "Review only - apply requires clean repositories"
    state = {
        "status": status,
        "classification": classification,
        "sourceHead": source_head,
        "sourceClean": source_clean,
        "targetHead": target_head,
        "targetClean": target_clean,
    }

    if not args.apply:
        render_report(state, entries, digest)
        print("Mode: review only; no files changed.")
        return 0

    if not eligible:
        render_report(state, entries, digest)
        print("ERROR: repository is not eligible for automatic brownfield apply", file=sys.stderr)
        return 1
    if not source_clean or not target_clean:
        render_report(state, entries, digest)
        print("ERROR: apply requires clean source and target repositories", file=sys.stderr)
        return 1
    expected = (
        args.expected_source_commit,
        args.expected_target_commit,
        args.expected_plan_digest,
    )
    if any(value is None for value in expected):
        print("ERROR: apply requires all expected source, target, and plan values", file=sys.stderr)
        return 2
    if args.expected_source_commit != source_head:
        print("ERROR: source commit differs from the reviewed commit", file=sys.stderr)
        return 2
    if args.expected_target_commit != target_head:
        print("ERROR: target commit differs from the reviewed commit", file=sys.stderr)
        return 2
    if args.expected_plan_digest != digest:
        print("ERROR: adoption plan differs from the reviewed plan", file=sys.stderr)
        return 2

    if git_head(source) != source_head or git_head(target) != target_head:
        print("ERROR: source or target commit moved after review verification", file=sys.stderr)
        return 2
    if not git_clean(source) or not git_clean(target):
        print("ERROR: source or target became dirty after review verification", file=sys.stderr)
        return 2

    try:
        applied = apply_adoption(
            source,
            target,
            source_manifest,
            source_metadata,
            entries,
            source_head,
            target_head,
        )
    except (OSError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    state["status"] = "Process layer seeded - manual reconciliation required"
    render_report(state, entries, digest, applied)
    return 0


if __name__ == "__main__":
    sys.exit(main())
