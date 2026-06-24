---
name: mamkin-context-reset
description: Run a same-thread Mamkin context reset by grounding the coordinator in current repo sources, stale assumptions, proof boundaries, and the next safe action.
---

# Mamkin Context Reset

Use this skill when the current coordinator thread is still usable but needs a source-grounded reset before more coordination, routing, implementation, or live validation.

## Workflow

1. Read `AGENTS.md`.
2. Read the context reset section in `docs/process/agent-orchestration.md`.
3. Read `docs/process/context-health-audit.md` if the reset was not already recommended by an audit.
4. Inspect current repo state with `pwd`, `git status --short --branch`, and `git rev-parse HEAD`.
5. Read current authoritative project sources needed for the lane: decision log, roadmap, relevant feature specs, follow-ups, walkthroughs, current reports, and returned packets only as evidence.
6. Produce a same-thread reset packet that states current authority, obsolete or historical assumptions, proof boundaries, safe next action, blockers, and what must not happen before reset acceptance.
7. Stop after the reset packet unless the user or coordinator explicitly assigns follow-up docs or routing.

## Boundaries

- This skill is read-only by default.
- Do not create a fresh coordinator thread. Use `mamkin-coordinator-rollover` when rollover is needed.
- Do not implement, merge, deploy, run live validation, or start write-capable workers during the reset.
- Old handoff packets, old summaries, generated reports, screenshots, and previous live checks are evidence only; current repo docs and human decisions decide authority.
- If the reset finds repeated source confusion or structural unreliability, recommend rollover instead of trying to repair the thread inline.

## Output Shape

Return a concise packet:

```text
Status: Context reset complete | Context reset blocked | Rollover recommended
Worktree:
Branch:
HEAD:
Sources read:
Current authority:
Current model:
Historical-only evidence:
Obsolete or unsafe assumptions:
Dirty repos/worktrees:
External proof boundary:
Next safe action:
Must not do next:
Human decisions needed:
Checks run:
```
