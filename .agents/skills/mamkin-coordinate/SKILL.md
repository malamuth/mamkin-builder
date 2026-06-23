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
5. Use the smallest useful team and start real specialists as separate threads by default.
6. Use `.codex/agents/mamkin-*.toml` presets when the platform supports custom agents.
7. Route human decisions through the coordinator unless a prompt explicitly delegates an exact specialist question.
8. Do not monitor active worker threads; wait for returned packets, blockers, human requests, or timeout recovery.
9. For approved coordinator rollover, follow the self-service rollover process in `docs/process/agent-orchestration.md`: create/send/verify the fresh coordinator, archive or rename the outgoing coordinator, and make the fresh thread the main coordinator when tools support it.
10. If context contamination is suspected, use `docs/process/context-health-audit.md` before choosing between normal continuation, watch, context reset, or rollover.

## Boundaries

- `docs/process/agent-orchestration.md` is the source of truth for coordination.
- Role cards and handoff packets stay in Markdown; this skill is only a discoverable entrypoint.
- If the project has not been initialized yet, run `mamkin-init` or follow `docs/process/init-agent.md` first.
