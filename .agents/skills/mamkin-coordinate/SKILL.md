---
name: mamkin-coordinate
description: Coordinate Mamkin Builder feature work after init. Use for coordinator flow, multi-agent planning, specialist routing, worker handoffs, walkthroughs, and implementation orchestration.
---

# Mamkin Coordinate

Use this skill when the project has already been initialized and the user wants coordinated feature work.

## Workflow

1. Read `AGENTS.md`.
2. Read and follow `docs/process/agent-orchestration.md`.
3. Read current project sources and only the conditional process docs named by the manual.
4. Use the smallest team and the manual's concrete role triggers.
5. Before delegation or two-track work, read `docs/process/execution-lane-routing.md`.
6. Wait for returned packets, blockers, human requests, or explicit recovery; do not poll active tasks.
7. Use the focused context audit, reset, or rollover skill when its trigger fires.

## Boundaries

- `docs/process/agent-orchestration.md` is the source of truth for coordination.
- This skill is a discoverable entrypoint, not a second coordination manual.
- If the project has not been initialized yet, run `mamkin-init` or follow `docs/process/init-agent.md` first.
