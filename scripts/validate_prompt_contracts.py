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
    git_delivery = ROOT / "docs/process/git-delivery.md"
    handoffs = ROOT / "docs/process/handoff-packets.md"
    config = ROOT / ".codex/config.toml"
    cases_path = ROOT / "evals/mamkin-prompt-cases.json"
    matrix_path = ROOT / "evals/mamkin-role-model-matrix.json"
    hooks_path = ROOT / ".codex/hooks.json"
    validation_map_path = ROOT / ".mamkin/validation-map.json"
    model_routing_path = ROOT / ".mamkin/model-routing.json"
    process_manifest_path = ROOT / ".mamkin/process-manifest.json"
    evolution_catalog_path = ROOT / ".mamkin/evolution-capabilities.json"
    version_path = ROOT / ".mamkin/template-version.json"
    evolution_skill = ROOT / ".agents/skills/mamkin-project-evolution-audit/SKILL.md"
    evolution_skill_ui = evolution_skill.parent / "agents/openai.yaml"
    evolution_protocol = ROOT / "docs/process/project-evolution-audit.md"
    evolution_packet = ROOT / "docs/process/handoff-packets/project-evolution-audit.md"
    adoption_skill = ROOT / ".agents/skills/mamkin-adopt/SKILL.md"
    adoption_skill_ui = adoption_skill.parent / "agents/openai.yaml"
    adoption_protocol = ROOT / "docs/process/adopt-existing-project.md"
    adoption_packet = ROOT / "docs/process/handoff-packets/adoption.md"
    bootstrap_skill = ROOT / ".agents/skills/mamkin-bootstrap/SKILL.md"
    bootstrap_skill_ui = bootstrap_skill.parent / "agents/openai.yaml"

    cases = json.loads(cases_path.read_text(encoding="utf-8"))
    if cases.get("schemaVersion") != 1:
        fail(errors, "prompt cases schemaVersion must be 1")
    entries = cases.get("cases") or []
    if len(entries) < 19:
        fail(errors, "prompt eval suite must contain at least 19 cases")

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
        "architect-required-shared-contract",
        "architect-skip-bounded-slice",
        "project-evolution-profit-gate",
        "project-evolution-no-auto-apply",
        "project-native-capability-ladder",
        "project-native-stale-learning",
        "brownfield-adoption-review",
        "brownfield-adoption-apply-gate",
        "portable-mamkin-bootstrap",
        "post-adoption-coordinator-start",
        "feature-git-delivery-gate",
        "authorized-git-closeout",
        "authorized-pr-closeout",
        "model-route-economy-inventory",
        "model-route-balanced-worker",
        "model-route-deep-diagnosis",
        "model-route-critical-review",
        "model-route-escalation",
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
        if experiment.get("decision") == "adopt-candidate" and experiment.get("status") != "passed":
            fail(errors, f"adopted model experiment {experiment.get('roleClass')} must have passed")
        experiment_case_ids = experiment.get("caseIds")
        if not experiment_case_ids or not set(experiment_case_ids).issubset(set(ids)):
            fail(errors, f"model experiment {experiment.get('roleClass')} needs known case ids")

    model_routing = json.loads(model_routing_path.read_text(encoding="utf-8"))
    expected_profiles = {
        "economy": ("gpt-5.6-terra", "medium", {"read-only": "mamkin-economy-read"}),
        "balanced": (
            "gpt-5.6-terra",
            "medium",
            {"read-only": "mamkin-balanced-read", "workspace-write": "mamkin-balanced-write"},
        ),
        "deep": (
            "gpt-5.6-sol",
            "high",
            {"read-only": "mamkin-deep-read", "workspace-write": "mamkin-deep-write"},
        ),
        "critical": (
            "gpt-5.6-sol",
            "xhigh",
            {"read-only": "mamkin-critical-read", "workspace-write": "mamkin-critical-write"},
        ),
    }
    if model_routing.get("schemaVersion") != 1:
        fail(errors, "model routing schemaVersion must be 1")
    if model_routing.get("profileOrder") != list(expected_profiles):
        fail(errors, "model routing profile order must be economy, balanced, deep, critical")
    if model_routing.get("maxPolicy") != "never-automatic":
        fail(errors, "model routing must never select max automatically")
    if model_routing.get("unavailableProfilePolicy") != "stop-no-silent-downgrade":
        fail(errors, "model routing must stop instead of silently downgrading")
    if set(model_routing.get("criticalSignals") or []) & set(model_routing.get("deepSignals") or []):
        fail(errors, "model routing critical and deep signals must be disjoint")
    if set(model_routing.get("economyRequirements") or []) != {
        "bounded",
        "deterministic-validation",
        "mechanical",
    }:
        fail(errors, "model routing economy requirements must remain bounded, deterministic, and mechanical")
    for profile_name, (model, effort, presets) in expected_profiles.items():
        profile = (model_routing.get("profiles") or {}).get(profile_name, {})
        if (profile.get("model"), profile.get("reasoningEffort"), profile.get("presets")) != (
            model,
            effort,
            presets,
        ):
            fail(errors, f"model routing profile {profile_name} does not match its accepted defaults")
        for access, preset_name in presets.items():
            preset_path = ROOT / f".codex/agents/{preset_name}.toml"
            if not preset_path.exists():
                fail(errors, f"model routing profile {profile_name} missing preset {preset_name}")
                continue
            preset_text = preset_path.read_text(encoding="utf-8")
            fields = dict(
                re.findall(
                    r'^(name|model|model_reasoning_effort|sandbox_mode)\s*=\s*"([^"]+)"\s*$',
                    preset_text,
                    flags=re.MULTILINE,
                )
            )
            if fields.get("name") != preset_name:
                fail(errors, f"profile preset {preset_name} has the wrong name")
            if fields.get("model") != model or fields.get("model_reasoning_effort") != effort:
                fail(errors, f"profile preset {preset_name} does not match model routing policy")
            if fields.get("sandbox_mode") != access:
                fail(errors, f"profile preset {preset_name} does not match access posture {access}")

    prompt_files = [agents, orchestration, lane_routing, handoffs]
    prompt_files += sorted((ROOT / ".codex/agents").glob("mamkin-*.toml"))
    prompt_files += sorted((ROOT / "docs/process/roles").glob("*.md"))
    prompt_files += sorted((ROOT / ".codex/hooks").glob("*.py"))
    prompt_files += sorted((ROOT / ".agents/skills").glob("mamkin-*/SKILL.md"))
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
    for phrase in [
        "Treat the current project repository and its assigned worktrees as the write boundary.",
        "an upstream Mamkin candidate is proposal-only",
        "or a template commit manufactured for the project's own sync",
    ]:
        if phrase not in agents_text:
            fail(errors, f"AGENTS.md missing repository-boundary invariant: {phrase}")
    if words(agents) > 750:
        fail(errors, f"AGENTS.md exceeds 750-word always-loaded budget ({words(agents)})")

    orchestration_text = orchestration.read_text(encoding="utf-8")
    core_contract_fields = [
        "Role:",
        "Reasoning profile:",
        "Profile trigger and risk floor:",
        "Agent preset / model / effort:",
        "Access posture:",
        "Escalation conditions:",
        "Goal:",
        "Success criteria:",
        "Required evidence and source authority:",
        "Scope and allowed files:",
        "Human and permission boundaries:",
        "Validation required:",
        "Output packet:",
        "Stop and fallback rules:",
        "Execution mode:",
        "Assigned return destination:",
        "Read first:",
    ]
    positions = [orchestration_text.find(field) for field in core_contract_fields]
    if any(position < 0 for position in positions) or positions != sorted(positions):
        fail(errors, "worker prompt core is missing outcome-first fields or has them out of order")
    core_start = orchestration_text.find("Every worker prompt includes this core:")
    core_end = orchestration_text.find("Add only applicable extensions.")
    core_block = orchestration_text[core_start:core_end]
    for conditional_field in ["Parent lane owner:", "Parallel track:", "Agent preset:", "Do not edit:"]:
        if conditional_field in core_block:
            fail(errors, f"worker prompt core contains conditional field {conditional_field}")
    for heading in [
        "### Separate-Task Extension",
        "### Subagent Extension",
        "### Write-Capable Extension",
        "### Parallel-Track Extension",
    ]:
        if heading not in orchestration_text:
            fail(errors, f"worker prompt contract missing conditional extension {heading}")
    if words(orchestration) > 3200:
        fail(errors, f"coordinator manual exceeds 3,200-word core budget ({words(orchestration)})")
    for phrase in [
        "Use an architect before implementation when any applies",
        "Skip the architect when all apply",
        "Do not include parallel fields for a single-track assignment",
        "Choose the role first, then select a reasoning profile from observable risk signals",
        "Never silently downgrade",
    ]:
        if phrase not in orchestration_text:
            fail(errors, f"coordinator manual missing optimization invariant: {phrase}")
    lane_text = lane_routing.read_text(encoding="utf-8")
    for phrase in [
        "Prefer a subagent when every subagent condition",
        "Use A Separate Task When Any Trigger Applies",
        "limited to tracks `A` and `B`",
        "Implementation and acceptance use different agents",
    ]:
        if phrase not in lane_text:
            fail(errors, f"execution lane routing missing invariant: {phrase}")
    coordinate_skill_text = (ROOT / ".agents/skills/mamkin-coordinate/SKILL.md").read_text(encoding="utf-8")
    for phrase in ["docs/process/model-routing.md", "trigger and risk floor"]:
        if phrase not in coordinate_skill_text:
            fail(errors, f"coordinate skill missing adaptive model-routing invariant: {phrase}")
    for vague_phrase in ["non-trivial slice", "trivial edit", "complex lane", "major routing"]:
        if vague_phrase in lane_text or vague_phrase in orchestration_text:
            fail(errors, f"routing still relies on vague threshold: {vague_phrase}")
    if words(lane_routing) > 1200:
        fail(errors, f"execution lane routing exceeds 1,200-word conditional budget ({words(lane_routing)})")

    git_delivery_text = git_delivery.read_text(encoding="utf-8")
    for phrase in [
        "Delivery mode: feature branch | direct-to-base exception",
        "Use `feature branch` by default",
        "Do not stash, reset, discard, or silently move a mixed worktree.",
        "At kickoff, the coordinator may ask once for exact external authority",
        "For `pull request`, push the feature branch and open/update the PR",
        "Do not locally integrate first.",
        "Do not rebase an accepted commit during closeout.",
        "Immediately before remote branch deletion, fetch/compare its tip again",
        "the result cannot be `Merge-ready` until an exact committed state exists",
        "After acceptance, the coordinator owns closeout",
        "Do not call a feature `Delivered` merely because implementation or walkthrough finished",
    ]:
        if phrase not in git_delivery_text:
            fail(errors, f"Git delivery protocol missing invariant: {phrase}")
    if words(git_delivery) > 1100:
        fail(errors, f"Git delivery protocol exceeds 1,100-word conditional budget ({words(git_delivery)})")

    feature_template_text = (ROOT / "docs/templates/feature-spec.md").read_text(encoding="utf-8")
    for field in [
        "## Git Delivery Contract",
        "Feature branch: `codex/fNN-short-scope`",
        "Direct-to-base rationale and approval:",
        "Integration path:",
        "Merge method:",
        "Remote and base target:",
        "External Git authority:",
        "Closeout owner: coordinator",
    ]:
        if field not in feature_template_text:
            fail(errors, f"feature template missing Git delivery field: {field}")

    coordinate_skill_text = (ROOT / ".agents/skills/mamkin-coordinate/SKILL.md").read_text(encoding="utf-8")
    if "Read `docs/process/naming-conventions.md` and `docs/process/handoff-packets.md`" in coordinate_skill_text:
        fail(errors, "coordinate skill still loads naming and packet indexes unconditionally")

    evolution_skill_text = evolution_skill.read_text(encoding="utf-8")
    if "[TODO" in evolution_skill_text:
        fail(errors, "project evolution audit skill still contains scaffold TODOs")
    for phrase in [
        "name: mamkin-project-evolution-audit",
        "Absence or a log entry alone is not a recommendation.",
        "Never create or update a project skill during the audit.",
        "Treat `Propose upstream` as a handoff-only result.",
        "Task creation authorizes reassessment only unless its starter scope explicitly authorizes implementation.",
        "Never edit, install, enable hooks, change models, create external resources, commit, or push",
    ]:
        if phrase not in evolution_skill_text:
            fail(errors, f"project evolution audit skill missing invariant: {phrase}")
    if words(evolution_skill) > 300:
        fail(errors, f"project evolution audit skill exceeds 300-word budget ({words(evolution_skill)})")
    evolution_ui_text = evolution_skill_ui.read_text(encoding="utf-8")
    for phrase in [
        'display_name: "Mamkin Project Evolution Audit"',
        'short_description: "Find profitable project and Mamkin process upgrades"',
        "$mamkin-project-evolution-audit",
    ]:
        if phrase not in evolution_ui_text:
            fail(errors, f"project evolution audit UI metadata missing: {phrase}")

    evolution_protocol_text = evolution_protocol.read_text(encoding="utf-8")
    for phrase in [
        "Net value = Benefit - Cost",
        "**Adopt now:**",
        "Do not recommend a hook",
        "Do not write the packet or apply recommendations.",
        "it is not an executable sync source",
        "Choose the smallest primary action:",
        "Create a project-local skill only for a distinct recurring invocation.",
        "must not leak project names, private targets, domain rules, or identifiers into Mamkin",
        "`Propose upstream` produces a proposal packet, never a cross-repository implementation.",
        "Approval to create that task authorizes reassessment only",
        "The copied-project task cannot create that exception for itself.",
    ]:
        if phrase not in evolution_protocol_text:
            fail(errors, f"project evolution audit protocol missing invariant: {phrase}")
    evolution_packet_text = evolution_packet.read_text(encoding="utf-8")
    for field in [
        "Adopt now:",
        "Bounded experiments:",
        "Do not adopt:",
        "Existing project mechanics to preserve:",
        "Project-specific knowledge that must not move upstream:",
        "Upstream proposals (handoff only; no template mutation in this task):",
        "Preferred action:",
        "Maintenance source and review/retirement trigger:",
        "Rollback:",
    ]:
        if field not in evolution_packet_text:
            fail(errors, f"project evolution audit packet missing field {field}")

    template_sync_skill_text = (ROOT / ".agents/skills/mamkin-template-sync/SKILL.md").read_text(encoding="utf-8")
    for phrase in [
        "Reject it as a sync source if the current copied-project task created or modified that checkout",
        "Local-only approval applies only to a pre-existing, provenance-declared source.",
    ]:
        if phrase not in template_sync_skill_text:
            fail(errors, f"template sync skill missing repository-boundary invariant: {phrase}")
    template_sync_protocol_text = (ROOT / "docs/process/template-sync.md").read_text(encoding="utf-8")
    for phrase in [
        "Provenance is an additional gate.",
        "Do not ask the human to bless that same-task cross-repository mutation after the fact.",
    ]:
        if phrase not in template_sync_protocol_text:
            fail(errors, f"template sync protocol missing repository-boundary invariant: {phrase}")

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
        for field in [
            "Execution mode:",
            "Parent lane owner:",
            "Parallel track:",
            "Reasoning profile used:",
            "Model and effort used:",
            "Profile trigger or escalation evidence:",
        ]:
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

    config_text = config.read_text(encoding="utf-8")
    if 'model_reasoning_effort = "medium"' not in config_text:
        fail(errors, "coordinator reasoning default must match the accepted medium experiment")
    for preset_name in ["mamkin-worker.toml", "mamkin-deployment.toml"]:
        preset_text = (ROOT / f".codex/agents/{preset_name}").read_text(encoding="utf-8")
        if 'model = "gpt-5.6-terra"' not in preset_text or 'model_reasoning_effort = "medium"' not in preset_text:
            fail(errors, f"{preset_name} must match the accepted Terra/medium experiment")
    for preset_name in [
        "mamkin-analyst.toml",
        "mamkin-architect.toml",
        "mamkin-reviewer.toml",
        "mamkin-walkthrough.toml",
        "mamkin-designer.toml",
        "mamkin-ux.toml",
    ]:
        preset_text = (ROOT / f".codex/agents/{preset_name}").read_text(encoding="utf-8")
        if 'model_reasoning_effort = "high"' not in preset_text:
            fail(errors, f"{preset_name} must remain high until role-specific execution evals pass")

    init_text = (ROOT / "docs/process/init-agent.md").read_text(encoding="utf-8")
    if "## Done Checklist" in init_text:
        fail(errors, "init-agent.md duplicates self-review with a Done Checklist")
    for phrase in ["focused rounds", "recommended default", "**Product proof**", "**Delivery shape**"]:
        if phrase not in init_text:
            fail(errors, f"init interview missing choice-first contract: {phrase}")
    if "## Manual Test Flows" in (ROOT / "docs/templates/feature-spec.md").read_text(encoding="utf-8"):
        fail(errors, "feature spec duplicates detailed walkthrough steps")

    adoption_skill_text = adoption_skill.read_text(encoding="utf-8")
    for phrase in [
        "name: mamkin-adopt",
        "Never overwrite an existing target file automatically.",
        "Apply no files until the human approves that exact plan.",
        "Adoption installs process only",
        "Do not begin product work in the adoption task unless the human explicitly chooses same-task continuation.",
    ]:
        if phrase not in adoption_skill_text:
            fail(errors, f"adoption skill missing invariant: {phrase}")
    if words(adoption_skill) > 320:
        fail(errors, f"adoption skill exceeds 320-word budget ({words(adoption_skill)})")
    adoption_ui_text = adoption_skill_ui.read_text(encoding="utf-8")
    for phrase in [
        'display_name: "Mamkin Adopt"',
        'short_description: "Safely adopt Mamkin in an existing project"',
        "$mamkin-adopt",
    ]:
        if phrase not in adoption_ui_text:
            fail(errors, f"adoption skill UI metadata missing: {phrase}")
    adoption_protocol_text = adoption_protocol.read_text(encoding="utf-8")
    for phrase in [
        "An existing target path always outranks upstream ownership.",
        "Re-review when the source commit, target commit, dirty state, or plan digest changes.",
        "Rolls back files created during the run when an apply error occurs.",
        "Adopted with baseline gaps",
        "Completed adoption is a durable context boundary",
        "This is a post-adoption coordinator start, not a coordinator rollover",
        "newly supplied feature requirements do not select either path",
        "Do not stash, reset, discard, or silently move them merely to unblock adoption.",
    ]:
        if phrase not in adoption_protocol_text:
            fail(errors, f"adoption protocol missing invariant: {phrase}")
    adoption_packet_text = adoption_packet.read_text(encoding="utf-8")
    for field in [
        "Target HEAD reviewed:",
        "Dirty-target recovery decision:",
        "Mamkin source commit:",
        "Existing collisions protected:",
        "Baseline failures or gaps:",
        "External configuration unchanged:",
        "First coordinator focus:",
        "Coordinator transition:",
        "Coordinator task id and title:",
        "Adoption task final state:",
    ]:
        if field not in adoption_packet_text:
            fail(errors, f"adoption packet missing field {field}")

    bootstrap_skill_text = bootstrap_skill.read_text(encoding="utf-8")
    for phrase in [
        "name: mamkin-bootstrap",
        "Do not copy this skill into the target manually",
        "https://github.com/malamuth/mamkin-builder.git",
        "Apply nothing until the human approves that exact plan.",
        "Do not stop after seeding files",
        "explicit coordinator-transition decision",
    ]:
        if phrase not in bootstrap_skill_text:
            fail(errors, f"bootstrap skill missing invariant: {phrase}")
    if words(bootstrap_skill) > 400:
        fail(errors, f"bootstrap skill exceeds 400-word budget ({words(bootstrap_skill)})")
    bootstrap_ui_text = bootstrap_skill_ui.read_text(encoding="utf-8")
    for phrase in [
        'display_name: "Mamkin Bootstrap"',
        'short_description: "Install Mamkin into any existing project"',
        "$mamkin-bootstrap",
    ]:
        if phrase not in bootstrap_ui_text:
            fail(errors, f"bootstrap skill UI metadata missing: {phrase}")
    for phrase in [
        "https://github.com/malamuth/mamkin-builder/tree/main/.agents/skills/mamkin-bootstrap",
        "The installed skill becomes available on the next turn.",
        "Do not manually copy a lone Mamkin skill into the target",
    ]:
        if phrase not in adoption_protocol_text:
            fail(errors, f"adoption protocol missing portable bootstrap contract: {phrase}")

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
        "adoption_tests",
        "prompt_contracts",
        "model_routing_tests",
        "validation_planner_tests",
        "template_sync_tests",
        "evolution_audit_tests",
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
        ".mamkin/evolution-capabilities.json",
        ".mamkin/validation-map.json",
        "docs/process/project-evolution-audit.md",
        "docs/process/adopt-existing-project.md",
        "docs/process/git-delivery.md",
        "docs/process/model-routing.md",
        "evals/mamkin-role-model-matrix.json",
        "scripts/audit_mamkin_evolution.py",
        "scripts/adopt_mamkin_process.py",
        "scripts/plan_validation.py",
        "scripts/select_model_profile.py",
        "scripts/sync_mamkin_process.py",
        "tests/test_audit_mamkin_evolution.py",
        "tests/test_adopt_mamkin_process.py",
        "tests/test_plan_validation.py",
        "tests/test_model_routing.py",
        "tests/test_sync_mamkin_process.py",
    ]:
        if path not in process_manifest.get("templateOwned", []):
            fail(errors, f"process manifest does not own {path}")
    if ".agents/skills/mamkin-*/**" not in process_manifest.get("templateOwned", []):
        fail(errors, "process manifest must include complete Mamkin skill packages")
    if ".mamkin/process-manifest.json" not in process_manifest.get("mixed", []):
        fail(errors, "process manifest must treat its own sync authority as mixed ownership")
    if ".mamkin/model-routing.json" not in process_manifest.get("mixed", []):
        fail(errors, "process manifest must treat model routing policy as mixed ownership")
    version = json.loads(version_path.read_text(encoding="utf-8"))
    if version.get("ownershipManifest") != ".mamkin/process-manifest.json":
        fail(errors, "template version must point to the machine-readable process manifest")

    evolution_catalog = json.loads(evolution_catalog_path.read_text(encoding="utf-8"))
    if evolution_catalog.get("schemaVersion") != 1:
        fail(errors, "evolution capability catalog schemaVersion must be 1")
    capabilities = evolution_catalog.get("capabilities") or []
    capability_ids = [capability.get("id") for capability in capabilities]
    if len(capabilities) < 11 or len(capability_ids) != len(set(capability_ids)):
        fail(errors, "evolution capability catalog needs at least eleven unique capabilities")
    if "project-native-capability-mining" not in capability_ids:
        fail(errors, "evolution capability catalog missing project-native capability mining")
    if "feature-git-delivery-contract" not in capability_ids:
        fail(errors, "evolution capability catalog missing feature Git delivery contract")
    for index, capability in enumerate(capabilities):
        for field in ["id", "title", "category", "paths", "benefitHypothesis"]:
            if not capability.get(field):
                fail(errors, f"evolution capability {index} missing {field}")
        for path in capability.get("paths") or []:
            if Path(path).is_absolute() or ".." in Path(path).parts:
                fail(errors, f"evolution capability {capability.get('id')} has unsafe path {path}")
        activation = capability.get("activation")
        if activation is not None:
            valid_predicates = {"equals", "notNull"} & set(activation)
            if not activation.get("path") or not isinstance(activation.get("jsonPath"), list):
                fail(errors, f"evolution capability {capability.get('id')} has invalid activation target")
            if len(valid_predicates) != 1:
                fail(errors, f"evolution capability {capability.get('id')} needs one activation predicate")

    for path in [
        bootstrap_skill,
        bootstrap_skill_ui,
        adoption_skill,
        adoption_skill_ui,
        adoption_protocol,
        adoption_packet,
        git_delivery,
        ROOT / "scripts/adopt_mamkin_process.py",
        evolution_skill,
        evolution_skill_ui,
        evolution_protocol,
        evolution_packet,
        evolution_catalog_path,
        ROOT / "scripts/audit_mamkin_evolution.py",
        ROOT / "README.md",
    ]:
        if "sambl" in path.read_text(encoding="utf-8").lower():
            fail(errors, f"{path.relative_to(ROOT)} leaks a project fixture into Mamkin")

    coordinator_default_paths = [
        agents,
        ROOT / ".agents/skills/mamkin-coordinate/SKILL.md",
        orchestration,
        ROOT / "docs/project/brief.md",
        ROOT / "docs/project/decision-log.md",
        ROOT / "features/00-roadmap.md",
    ]
    conditional_delegation_paths = [
        ROOT / "docs/process/naming-conventions.md",
        handoffs,
        lane_routing,
        git_delivery,
        ROOT / "docs/process/model-routing.md",
        ROOT / "docs/process/thread-operations.md",
    ]
    metrics = {
        "agents_words": words(agents),
        "orchestration_words": words(orchestration),
        "execution_lane_routing_words": words(lane_routing),
        "git_delivery_words": words(git_delivery),
        "coordinator_default_words": sum(words(path) for path in coordinator_default_paths),
        "coordinator_delegation_words": sum(
            words(path) for path in coordinator_default_paths + conditional_delegation_paths
        ),
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
