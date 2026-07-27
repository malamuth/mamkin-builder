#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def words(path):
    return len(path.read_text(encoding="utf-8").split())


def fail(errors, message):
    errors.append(message)


def main():
    errors = []
    agents = ROOT / "AGENTS.md"
    orchestration = ROOT / "docs/process/agent-orchestration.md"
    lane_routing = ROOT / "docs/process/execution-lane-routing.md"
    handoffs = ROOT / "docs/process/handoff-packets.md"
    config = ROOT / ".codex/config.toml"
    cases_path = ROOT / "evals/mamkin-prompt-cases.json"
    matrix_path = ROOT / "evals/mamkin-role-model-matrix.json"
    hooks_path = ROOT / ".codex/hooks.json"
    validation_map_path = ROOT / ".mamkin/validation-map.json"
    process_manifest_path = ROOT / ".mamkin/process-manifest.json"
    version_path = ROOT / ".mamkin/template-version.json"

    cases = json.loads(cases_path.read_text(encoding="utf-8"))
    if cases.get("schemaVersion") != 1:
        fail(errors, "prompt cases schemaVersion must be 1")
    entries = cases.get("cases") or []
    if len(entries) < 13:
        fail(errors, "prompt eval suite must contain at least 13 cases")

    ids = []
    required_case = {"id", "title", "request", "setup", "expected"}
    required_expected = {
        "actionMode",
        "humanConfirmation",
        "requiredBehavior",
        "forbiddenBehavior",
        "completion",
    }
    for index, case in enumerate(entries):
        missing = required_case - set(case)
        if missing:
            fail(errors, f"case {index} missing fields: {sorted(missing)}")
            continue
        ids.append(case["id"])
        missing_expected = required_expected - set(case["expected"])
        if missing_expected:
            fail(errors, f"case {case['id']} missing expected fields: {sorted(missing_expected)}")
    if len(ids) != len(set(ids)):
        fail(errors, "prompt eval case ids must be unique")
    required_ids = {
        "subagent-preferred",
        "separate-task-trigger",
        "two-track-admission",
        "two-track-hidden-conflict",
        "two-track-cap",
    }
    missing_ids = required_ids - set(ids)
    if missing_ids:
        fail(errors, f"prompt eval suite missing execution-lane cases: {sorted(missing_ids)}")

    matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    if matrix.get("schemaVersion") != 1 or matrix.get("status") != "experiments-only":
        fail(errors, "role model matrix must be schemaVersion 1 and experiments-only")
    dimensions = set(matrix.get("qualityGate", {}).get("dimensions", []))
    if dimensions != {"outcome", "scope", "evidence", "permissions", "validation", "handoff"}:
        fail(errors, "role model matrix quality gate must use the prompt eval rubric")
    experiments = matrix.get("experiments") or []
    role_classes = [experiment.get("roleClass") for experiment in experiments]
    if len(experiments) < 4 or len(role_classes) != len(set(role_classes)):
        fail(errors, "role model matrix needs at least four unique role classes")
    for experiment in experiments:
        for field in ("baseline", "candidate", "status", "decision"):
            if field not in experiment:
                fail(errors, f"model experiment {experiment.get('roleClass')} missing {field}")
        if experiment.get("status") == "not-run" and experiment.get("decision") != "keep-baseline":
            fail(errors, f"unrun model experiment {experiment.get('roleClass')} must keep baseline")
        experiment_case_ids = experiment.get("caseIds")
        if not experiment_case_ids or not set(experiment_case_ids).issubset(set(ids)):
            fail(errors, f"model experiment {experiment.get('roleClass')} needs known case ids")

    prompt_files = [agents, orchestration, lane_routing, handoffs]
    prompt_files += sorted((ROOT / ".codex/agents").glob("mamkin-*.toml"))
    prompt_files += sorted((ROOT / "docs/process/roles").glob("*.md"))
    prompt_files += sorted((ROOT / ".codex/hooks").glob("*.py"))
    relay_phrase = "Coordinator handoff - manual relay required"
    relay_hits = sum(path.read_text(encoding="utf-8").count(relay_phrase) for path in prompt_files)
    if relay_hits > 2:
        fail(errors, f"manual-relay invariant is duplicated {relay_hits} times in active prompt files")

    hooks = json.loads(hooks_path.read_text(encoding="utf-8"))
    if "SubagentStart" in hooks.get("hooks", {}):
        fail(errors, "SubagentStart must not inject a second worker workflow contract")
    if (ROOT / ".codex/hooks/subagent_start_context.py").exists():
        fail(errors, "obsolete subagent_start_context.py still exists")

    agents_text = agents.read_text(encoding="utf-8")
    for heading in ["## Autonomy And Human Gates", "## Repository Safety And Evidence", "## Worker Handoff Contract"]:
        if heading not in agents_text:
            fail(errors, f"AGENTS.md missing {heading}")
    if words(agents) > 750:
        fail(errors, f"AGENTS.md exceeds 750-word always-loaded budget ({words(agents)})")

    orchestration_text = orchestration.read_text(encoding="utf-8")
    contract_fields = [
        "Role:",
        "Goal:",
        "Success criteria:",
        "Required evidence and source authority:",
        "Scope and allowed files:",
        "Validation required:",
        "Output packet:",
        "Stop and fallback rules:",
        "Execution mode:",
        "Parent lane owner:",
        "Subagents:",
        "Parallel track:",
    ]
    positions = [orchestration_text.find(field) for field in contract_fields]
    if any(position < 0 for position in positions) or positions != sorted(positions):
        fail(errors, "worker prompt contract is missing outcome-first fields or has them out of order")
    if words(orchestration) > 4200:
        fail(errors, f"coordinator manual exceeds 4,200-word core budget ({words(orchestration)})")
    lane_text = lane_routing.read_text(encoding="utf-8")
    for phrase in [
        "Prefer a subagent when every subagent condition",
        "Use A Separate Task When Any Trigger Applies",
        "limited to tracks `A` and `B`",
        "Implementation and acceptance use different agents",
    ]:
        if phrase not in lane_text:
            fail(errors, f"execution lane routing missing invariant: {phrase}")
    if words(lane_routing) > 1200:
        fail(errors, f"execution lane routing exceeds 1,200-word conditional budget ({words(lane_routing)})")

    for role in sorted((ROOT / "docs/process/roles").glob("*.md")):
        text = role.read_text(encoding="utf-8")
        if "Follow the Worker Handoff Contract in `AGENTS.md`. Return one packet, then stop." not in text:
            fail(errors, f"{role.relative_to(ROOT)} does not use the central worker contract")
        if words(role) > 500:
            fail(errors, f"{role.relative_to(ROOT)} exceeds 500-word role-card budget ({words(role)})")

    role_contracts = {
        "analyst": ("mamkin-analyst.toml", ["analysis.md"]),
        "architect": ("mamkin-architect.toml", ["architecture.md"]),
        "deployment": ("mamkin-deployment.toml", ["deployment.md"]),
        "designer": ("mamkin-designer.toml", ["designer.md"]),
        "implementation": ("mamkin-worker.toml", ["implementation.md"]),
        "reviewer": ("mamkin-reviewer.toml", ["reviewer.md"]),
        "ux": ("mamkin-ux.toml", ["ux.md"]),
        "walkthrough": (
            "mamkin-walkthrough.toml",
            ["walkthrough-defect.md", "walkthrough-readiness.md"],
        ),
    }
    for role_name, (preset_name, packet_names) in role_contracts.items():
        if not (ROOT / f"docs/process/roles/{role_name}.md").exists():
            fail(errors, f"missing built-in role card for {role_name}")
        if not (ROOT / f".codex/agents/{preset_name}").exists():
            fail(errors, f"role {role_name} missing preset {preset_name}")
        for packet_name in packet_names:
            if not (ROOT / f"docs/process/handoff-packets/{packet_name}").exists():
                fail(errors, f"role {role_name} missing packet {packet_name}")

    worker_packets = [
        ROOT / "docs/process/handoff-packets/analysis.md",
        ROOT / "docs/process/handoff-packets/architecture.md",
        ROOT / "docs/process/handoff-packets/deployment.md",
        ROOT / "docs/process/handoff-packets/designer.md",
        ROOT / "docs/process/handoff-packets/implementation.md",
        ROOT / "docs/process/handoff-packets/reviewer.md",
        ROOT / "docs/process/handoff-packets/ux.md",
        ROOT / "docs/process/handoff-packets/walkthrough-defect.md",
        ROOT / "docs/process/handoff-packets/walkthrough-readiness.md",
        ROOT / "docs/templates/handoff-packet.md",
    ]
    for packet in worker_packets:
        text = packet.read_text(encoding="utf-8")
        for field in ["Execution mode:", "Parent lane owner:", "Parallel track:"]:
            if field not in text:
                fail(errors, f"{packet.relative_to(ROOT)} missing execution-lane field {field}")
        if words(packet) > 250:
            fail(errors, f"{packet.relative_to(ROOT)} exceeds 250-word packet budget ({words(packet)})")

    reviewer_packet = (ROOT / "docs/process/handoff-packets/reviewer.md").read_text(encoding="utf-8")
    for field in ["Severity:", "Location:", "Failure mode:", "Evidence:", "Smallest safe correction:"]:
        if field not in reviewer_packet:
            fail(errors, f"reviewer packet missing finding field {field}")
    walkthrough_template = (ROOT / "docs/templates/walkthrough.md").read_text(encoding="utf-8")
    for scenario in [
        "Success",
        "Failure and recovery",
        "Boundary",
        "Repeated or idempotent action",
        "Persistence or state transition",
        "Retry or cancellation",
        "Stale or partial input",
    ]:
        if scenario not in walkthrough_template:
            fail(errors, f"walkthrough template missing risk scenario {scenario}")

    preset_words = {}
    for preset in sorted((ROOT / ".codex/agents").glob("mamkin-*.toml")):
        count = words(preset)
        preset_words[str(preset.relative_to(ROOT))] = count
        if count > 120:
            fail(errors, f"{preset.relative_to(ROOT)} exceeds 120-word wrapper budget ({count})")

    init_text = (ROOT / "docs/process/init-agent.md").read_text(encoding="utf-8")
    if "## Done Checklist" in init_text:
        fail(errors, "init-agent.md duplicates self-review with a Done Checklist")
    for phrase in ["focused rounds", "recommended default", "**Product proof**", "**Delivery shape**"]:
        if phrase not in init_text:
            fail(errors, f"init interview missing choice-first contract: {phrase}")
    if "## Manual Test Flows" in (ROOT / "docs/templates/feature-spec.md").read_text(encoding="utf-8"):
        fail(errors, "feature spec duplicates detailed walkthrough steps")

    validation_map = json.loads(validation_map_path.read_text(encoding="utf-8"))
    if validation_map.get("schemaVersion") != 1:
        fail(errors, "validation map schemaVersion must be 1")
    checks = validation_map.get("checks") or {}
    post_edit = validation_map.get("postEdit") or {}
    if post_edit.get("mode") != "disabled" or post_edit.get("command") is not None:
        fail(errors, "template postEdit formatter must default to disabled with no command")
    hooks_text = hooks_path.read_text(encoding="utf-8")
    if "post_edit_format.py" not in hooks_text:
        fail(errors, "PostToolUse must route through the optional post-edit formatter")
    for required_check in [
        "diff_check",
        "prompt_contracts",
        "validation_planner_tests",
        "template_sync_tests",
        "project_check",
    ]:
        if required_check not in checks:
            fail(errors, f"validation map missing {required_check}")
    if checks.get("project_check", {}).get("command", "missing") is not None:
        fail(errors, "template project_check must remain unconfigured until init")
    for check_id, entry in checks.items():
        command = entry.get("command")
        if command is not None and (
            not isinstance(command, list)
            or not command
            or not all(isinstance(part, str) and part for part in command)
        ):
            fail(errors, f"validation check {check_id} must use a non-empty argv array")

    process_manifest = json.loads(process_manifest_path.read_text(encoding="utf-8"))
    if process_manifest.get("schemaVersion") != 1:
        fail(errors, "process manifest schemaVersion must be 1")
    ownership_values = {}
    for ownership in ["templateOwned", "mixed", "projectOwned", "neverSync"]:
        patterns = process_manifest.get(ownership)
        if not isinstance(patterns, list) or not patterns:
            fail(errors, f"process manifest {ownership} must be a non-empty list")
            continue
        for pattern in patterns:
            if pattern in ownership_values:
                fail(errors, f"process manifest duplicates {pattern} across ownership classes")
            ownership_values[pattern] = ownership
    for path in [
        ".mamkin/validation-map.json",
        "evals/mamkin-role-model-matrix.json",
        "scripts/plan_validation.py",
        "scripts/sync_mamkin_process.py",
        "tests/test_plan_validation.py",
        "tests/test_sync_mamkin_process.py",
    ]:
        if path not in process_manifest.get("templateOwned", []):
            fail(errors, f"process manifest does not own {path}")
    if ".mamkin/process-manifest.json" not in process_manifest.get("mixed", []):
        fail(errors, "process manifest must treat its own sync authority as mixed ownership")
    version = json.loads(version_path.read_text(encoding="utf-8"))
    if version.get("ownershipManifest") != ".mamkin/process-manifest.json":
        fail(errors, "template version must point to the machine-readable process manifest")

    coordinator_paths = [
        agents,
        ROOT / ".agents/skills/mamkin-coordinate/SKILL.md",
        orchestration,
        ROOT / "docs/process/naming-conventions.md",
        handoffs,
        ROOT / "docs/project/brief.md",
        ROOT / "docs/project/decision-log.md",
        ROOT / "features/00-roadmap.md",
    ]
    metrics = {
        "agents_words": words(agents),
        "orchestration_words": words(orchestration),
        "execution_lane_routing_words": words(lane_routing),
        "coordinator_default_words": sum(words(path) for path in coordinator_paths),
        "manual_relay_occurrences": relay_hits,
        "high_reasoning_settings": len(re.findall(r'model_reasoning_effort\s*=\s*"high"', config.read_text(encoding="utf-8") + "\n" + "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / ".codex/agents").glob("mamkin-*.toml")))),
        "eval_cases": len(entries),
        "preset_words": preset_words,
    }
    print(json.dumps(metrics, indent=2, sort_keys=True))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Prompt contract validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
