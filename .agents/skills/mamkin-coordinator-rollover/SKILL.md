---
name: mamkin-coordinator-rollover
description: Execute an approved Mamkin coordinator rollover into a fresh coordinator thread using the reset baseline, thread tools when available, and manual fallback when needed.
---

# Mamkin Coordinator Rollover

Use this skill when the human approves coordinator rollover, or when `mamkin-context-audit` or `mamkin-context-reset` recommends rollover and the human asks to proceed.

## Workflow

1. Read `AGENTS.md`.
2. Read the coordinator rollover section in `docs/process/agent-orchestration.md`.
3. Read `docs/process/handoff-packets/coordinator-reset.md`.
4. Read `docs/process/naming-conventions.md`.
5. Inspect current repo state with `pwd`, `git status --short --branch`, and `git rev-parse HEAD`.
6. Confirm there is a reset baseline: a committed reset doc, a coordinator reset packet, or a freshly prepared source-grounded packet.
7. If thread-management tools are available, create or start the fresh coordinator thread, send the starter prompt, verify receipt when possible, archive/rename the outgoing coordinator, and promote the fresh coordinator to the main coordinator title.
8. If thread-management tools are unavailable or blocked, return the exact manual starter prompt for the human to paste and clearly label this as fallback.
9. Report the new coordinator thread id when known, baseline commit/doc, old-thread cleanup status, and whether the next write-capable slice needs a branch/worktree.

## Boundaries

- Do not run rollover without human approval unless the user prompt explicitly delegates that action.
- Rollover is not a Git-branching action. Create a branch/worktree only for the next write-capable slice when isolation is needed.
- The outgoing coordinator transfers authority and then stops coordinating future work.
- Do not implement, merge, deploy, run live validation, or start write-capable workers during rollover.
- Do not leave two active-looking coordinator threads when title/archive tools are available.
- If create/send works but rename/archive is unavailable, mark old-thread cleanup as manual and stop using the outgoing thread for coordination.

## Output Shape

Return or send a coordinator reset/rollover packet using `docs/process/handoff-packets/coordinator-reset.md`, including:

```text
Status:
Old coordinator thread id:
New coordinator thread id, if known:
Rollover execution path:
Main coordinator after rollover:
Baseline commit or exact state:
Starter prompt sent:
Fresh coordinator receipt verified:
Old coordinator archived/renamed:
Old coordinator final status:
Recommended next action:
```
