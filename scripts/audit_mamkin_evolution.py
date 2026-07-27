#!/usr/bin/env python3
"""Inventory Mamkin capability gaps in a mature project without modifying it."""

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = ".mamkin/evolution-capabilities.json"
VERSION_PATH = ".mamkin/template-version.json"

SIGNAL_PATTERNS = {
    "manual-workaround": ["manual", "workaround", "hand-edit", "copy by hand"],
    "validation-friction": ["validation gap", "missing check", "check failed", "not validated"],
    "handoff-friction": ["handoff", "manual relay", "wrong thread", "retest"],
    "context-friction": ["context drift", "stale assumption", "rollover", "context reset"],
    "automation-candidate": ["repeated step", "automate", "hook", "formatting"],
}


def run_git(root, *args):
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def git_state(root):
    head = run_git(root, "rev-parse", "HEAD")
    branch = run_git(root, "branch", "--show-current")
    status = run_git(root, "status", "--short")
    commit_count = run_git(root, "rev-list", "--count", "HEAD")
    return {
        "available": head is not None,
        "branch": branch or None,
        "head": head,
        "dirty": bool(status) if status is not None else None,
        "status": status.splitlines() if status else [],
        "commitCount": int(commit_count) if commit_count and commit_count.isdigit() else None,
    }


def read_json(path, default=None):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def json_value(document, path):
    current = document
    for part in path:
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def activation_state(project, activation):
    if not activation:
        return None
    document = read_json(project / activation["path"])
    if document is None:
        return False
    value = json_value(document, activation.get("jsonPath", []))
    if activation.get("notNull"):
        return value is not None
    if "equals" in activation:
        return value == activation["equals"]
    return bool(value)


def capability_inventory(project, template, catalog):
    inventory = []
    for capability in catalog["capabilities"]:
        paths = capability["paths"]
        project_present = [path for path in paths if (project / path).is_file()]
        template_present = [path for path in paths if (template / path).is_file()]
        missing = [path for path in paths if path not in project_present]
        if not project_present:
            state = "missing"
        elif missing:
            state = "partial"
        else:
            active = activation_state(project, capability.get("activation"))
            state = "inactive" if active is False else "present"
        inventory.append(
            {
                "id": capability["id"],
                "title": capability["title"],
                "category": capability["category"],
                "state": state,
                "projectPathsPresent": project_present,
                "projectPathsMissing": missing,
                "templateAvailable": len(template_present) == len(paths),
                "templatePathsMissing": [
                    path for path in paths if path not in template_present
                ],
                "benefitHypothesis": capability["benefitHypothesis"],
            }
        )
    return inventory


def relative_files(root, pattern):
    return sorted(path.relative_to(root).as_posix() for path in root.glob(pattern) if path.is_file())


def project_customizations(project):
    skills = [
        path
        for path in relative_files(project, ".agents/skills/*/SKILL.md")
        if not path.split("/")[2].startswith("mamkin-")
    ]
    agents = [
        path
        for path in relative_files(project, ".codex/agents/*.toml")
        if not Path(path).name.startswith("mamkin-")
    ]
    hooks = read_json(project / ".codex/hooks.json", {}) or {}
    validation = read_json(project / ".mamkin/validation-map.json", {}) or {}
    project_check = (
        validation.get("checks", {}).get("project_check", {}).get("command")
        if validation
        else None
    )
    return {
        "customSkills": skills,
        "customAgents": agents,
        "hookEvents": sorted((hooks.get("hooks") or {}).keys()),
        "projectValidationConfigured": project_check is not None,
        "projectValidationCommand": project_check,
    }


def maturity(project):
    feature_files = [
        path
        for path in relative_files(project, "features/[0-9][0-9]-*.md")
        if not path.endswith("00-roadmap.md")
    ]
    return {
        "featureSpecs": len(feature_files),
        "walkthroughs": len(relative_files(project, "docs/walkthroughs/**/*.md")),
        "followUps": len(relative_files(project, "docs/follow-ups/**/*.md")),
        "decisionLogPresent": (project / "docs/project/decision-log.md").is_file(),
    }


def signal_files(project):
    candidates = []
    fixed = [project / "docs/project/decision-log.md"]
    fixed.extend(project.glob("docs/follow-ups/**/*.md"))
    fixed.extend(project.glob("docs/project/**/*notes*.md"))
    for path in fixed:
        if path.is_file() and path not in candidates:
            candidates.append(path)
        if len(candidates) >= 200:
            break
    return candidates


def text_signals(project):
    results = {
        signal: {"occurrences": 0, "files": []} for signal in SIGNAL_PATTERNS
    }
    total_bytes = 0
    for path in signal_files(project):
        try:
            size = path.stat().st_size
            if total_bytes + size > 2_000_000:
                break
            text = path.read_text(encoding="utf-8").lower()
        except OSError:
            continue
        total_bytes += size
        relative = path.relative_to(project).as_posix()
        for signal, patterns in SIGNAL_PATTERNS.items():
            count = sum(text.count(pattern) for pattern in patterns)
            if count:
                results[signal]["occurrences"] += count
                results[signal]["files"].append(relative)
    return {"scannedBytes": total_bytes, "signals": results}


def baseline_distance(template, metadata):
    baseline = metadata.get("lastProcessSyncCommit") or metadata.get("templateCommit")
    if not baseline or baseline == "TBD":
        return {
            "baseline": baseline or None,
            "available": False,
            "ancestor": None,
            "commitsBehind": None,
        }
    valid = run_git(template, "cat-file", "-e", f"{baseline}^{{commit}}")
    if valid is None:
        return {
            "baseline": baseline,
            "available": False,
            "ancestor": None,
            "commitsBehind": None,
        }
    ancestor = run_git(template, "merge-base", "--is-ancestor", baseline, "HEAD")
    if ancestor is None:
        return {
            "baseline": baseline,
            "available": True,
            "ancestor": False,
            "commitsBehind": None,
        }
    count = run_git(template, "rev-list", "--count", f"{baseline}..HEAD")
    return {
        "baseline": baseline,
        "available": True,
        "ancestor": True,
        "commitsBehind": int(count) if count and count.isdigit() else None,
    }


def build_inventory(project, template, catalog):
    metadata = read_json(project / VERSION_PATH, {}) or {}
    return {
        "schemaVersion": 1,
        "mode": "read-only-inventory",
        "project": {
            "path": str(project),
            "git": git_state(project),
            "templateMetadata": metadata,
            "maturity": maturity(project),
            "customizations": project_customizations(project),
            "textSignals": text_signals(project),
        },
        "template": {
            "path": str(template),
            "git": git_state(template),
            "baselineDistance": baseline_distance(template, metadata),
        },
        "capabilities": capability_inventory(project, template, catalog),
        "proofBoundary": [
            "Presence, absence, activation state, and bounded text counts are deterministic.",
            "Text counts indicate recurrence only and require source inspection before recommendation.",
            "No capability is recommended by this inventory.",
        ],
    }


def render_markdown(inventory):
    project = inventory["project"]
    template = inventory["template"]
    lines = [
        "# Mamkin Evolution Inventory",
        "",
        f"- Project: `{project['path']}`",
        f"- Project HEAD: `{project['git']['head'] or 'unavailable'}`",
        f"- Project dirty: `{project['git']['dirty']}`",
        f"- Template: `{template['path']}`",
        f"- Template HEAD: `{template['git']['head'] or 'unavailable'}`",
        f"- Recorded baseline: `{template['baselineDistance']['baseline'] or 'unknown'}`",
        f"- Baseline is template ancestor: `{template['baselineDistance']['ancestor']}`",
        f"- Commits behind: `{template['baselineDistance']['commitsBehind']}`",
        "",
        "## Capability States",
        "",
        "| Capability | Category | State |",
        "| --- | --- | --- |",
    ]
    for item in inventory["capabilities"]:
        lines.append(f"| {item['title']} | {item['category']} | {item['state']} |")
    lines.extend(
        [
            "",
            "This is a read-only inventory, not a recommendation report.",
        ]
    )
    return "\n".join(lines) + "\n"


def validate_catalog(catalog):
    if not isinstance(catalog, dict) or catalog.get("schemaVersion") != 1:
        raise ValueError("capability catalog schemaVersion must be 1")
    capabilities = catalog.get("capabilities")
    if not isinstance(capabilities, list) or not capabilities:
        raise ValueError("capability catalog must contain capabilities")
    ids = []
    for entry in capabilities:
        required = {"id", "title", "category", "paths", "benefitHypothesis"}
        missing = required - set(entry)
        if missing:
            raise ValueError(f"capability missing fields: {sorted(missing)}")
        if not entry["paths"] or not all(
            isinstance(path, str)
            and path
            and not Path(path).is_absolute()
            and ".." not in Path(path).parts
            for path in entry["paths"]
        ):
            raise ValueError(f"capability {entry['id']} paths must be relative")
        activation = entry.get("activation")
        if activation is not None:
            predicates = {"equals", "notNull"} & set(activation)
            activation_path = activation.get("path")
            if (
                not isinstance(activation_path, str)
                or not activation_path
                or Path(activation_path).is_absolute()
                or ".." in Path(activation_path).parts
                or not isinstance(activation.get("jsonPath"), list)
                or len(predicates) != 1
            ):
                raise ValueError(f"capability {entry['id']} activation is invalid")
        ids.append(entry["id"])
    if len(ids) != len(set(ids)):
        raise ValueError("capability ids must be unique")


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--template", default=str(ROOT))
    parser.add_argument("--catalog")
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    args = parser.parse_args(argv)

    project = Path(args.project).resolve()
    template = Path(args.template).resolve()
    catalog_path = (
        Path(args.catalog).resolve()
        if args.catalog
        else template / DEFAULT_CATALOG
    )
    if not project.is_dir() or not template.is_dir():
        print("ERROR: project and template must be existing directories", file=sys.stderr)
        return 2
    catalog = read_json(catalog_path)
    try:
        validate_catalog(catalog)
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2

    inventory = build_inventory(project, template, catalog)
    if args.format == "markdown":
        print(render_markdown(inventory), end="")
    else:
        print(json.dumps(inventory, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
