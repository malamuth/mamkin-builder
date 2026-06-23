---
name: mamkin-context-audit
description: Audit whether a Mamkin coordinator context is healthy, at risk, needs a source-grounded context reset, or should roll over to a fresh coordinator thread.
---

# Mamkin Context Audit

Use this skill when the user asks whether coordinator context is contaminated, drifting, hallucinating, over-focused on stale details, or ready for rollover.

## Workflow

1. Read `AGENTS.md`.
2. Read `docs/process/context-health-audit.md`.
3. Read the context reset and coordinator rollover sections in `docs/process/agent-orchestration.md`.
4. Inspect current repo state with `pwd`, `git status --short --branch`, and `git rev-parse HEAD`.
5. Read current project sources needed for the audited lane: decision log, roadmap, feature specs, follow-ups, walkthroughs, and returned packets only as needed.
6. If the user provides or asks you to inspect Codex thread ids, read only the relevant recent turns. Do not steer the audited threads unless explicitly asked.
7. Return the audit packet from `docs/process/context-health-audit.md`.

## Boundaries

- This skill is read-only by default.
- Do not run context reset or rollover from this skill. Recommend the smallest safe escalation.
- `watch` is an explicit status: continue carefully, name the risk, and state the trigger that would require reset.
- Context reset keeps the same coordinator thread and requires a source-grounded restatement before more action.
- Rollover creates/promotes a fresh coordinator thread using the process in `docs/process/agent-orchestration.md`.
