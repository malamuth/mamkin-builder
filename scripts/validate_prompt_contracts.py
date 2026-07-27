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
    hooks_path = ROOT / ".codex/hooks.json"

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

    preset_words = {}
    for preset in sorted((ROOT / ".codex/agents").glob("mamkin-*.toml")):
        count = words(preset)
        preset_words[str(preset.relative_to(ROOT))] = count
        if count > 120:
            fail(errors, f"{preset.relative_to(ROOT)} exceeds 120-word wrapper budget ({count})")

    if "## Done Checklist" in (ROOT / "docs/process/init-agent.md").read_text(encoding="utf-8"):
        fail(errors, "init-agent.md duplicates self-review with a Done Checklist")
    if "## Manual Test Flows" in (ROOT / "docs/templates/feature-spec.md").read_text(encoding="utf-8"):
        fail(errors, "feature spec duplicates detailed walkthrough steps")

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
