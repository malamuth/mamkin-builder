---
name: mamkin-coordinate
description: Coordinate Mamkin Builder feature work after init. Use for coordinator flow, multi-agent planning, specialist routing, worker handoffs, walkthroughs, and implementation orchestration.
---

# Mamkin Coordinate

Use this skill when the project has already been initialized and the user wants coordinated feature work.

## Workflow

1. Read `AGENTS.md`.
2. Read and follow `docs/process/agent-orchestration.md`.
3. Read `docs/process/naming-conventions.md` and `docs/process/handoff-packets.md`.
4. Read the project brief, decision log, roadmap, relevant feature specs, follow-ups, and walkthroughs as needed.
5. Read `docs/process/execution-lane-routing.md` when choosing between a subagent and a separate task, or when the human requests two independent work tracks.
6. Use the smallest useful team. Prefer a subagent when every subagent condition passes; use a separate task when any separate-task trigger applies.
7. Limit parallel feature work to two admitted tracks with one project coordinator.
8. Use `.codex/agents/mamkin-*.toml` presets when the platform supports custom agents.
9. Route human decisions through the coordinator unless a prompt explicitly delegates an exact specialist question.
10. Do not monitor active worker tasks; wait for returned packets, blockers, human requests, or timeout recovery.
11. For approved coordinator rollover, use `mamkin-coordinator-rollover` or follow the self-service rollover process in `docs/process/agent-orchestration.md`: create/send/verify the fresh coordinator, archive or rename the outgoing coordinator, and make the fresh task the main coordinator when tools support it.
12. If context contamination is suspected, use `docs/process/context-health-audit.md` or `mamkin-context-audit` before choosing between normal continuation, watch, context reset, or rollover.
13. For a same-thread source-grounded reset, use `mamkin-context-reset`.

## Boundaries

- `docs/process/agent-orchestration.md` is the source of truth for coordination.
- Role cards and handoff packets stay in Markdown; this skill is only a discoverable entrypoint.
- If the project has not been initialized yet, run `mamkin-init` or follow `docs/process/init-agent.md` first.
