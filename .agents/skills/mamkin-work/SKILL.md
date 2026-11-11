---
name: mamkin-work
description: Execute or resume authorized Mamkin 2.0 tasks in Codex using a backlog or ordered stages, preserving progress across chats.
---

# Mamkin Work

Complete the authorized work or report its concrete stop condition. Use `docs/mamkin/project.md` and `docs/mamkin/work.md` as entrypoints, following authoritative links only as needed. Recover missing context from current sources; ask only for essential missing decisions.

## Choose and reconcile

Separate scheduling mode from authorization. Default to one task; use backlog ordering when no other mode is declared. Preserve the user's priorities, dependencies, phase order and exit criteria. A mode or a list of tasks alone never grants a whole-queue run.

Resolve the current request and any unchanged explicit continuation grant: one task, a named current phase, or a defined queue. Preserve applicable limits and already admitted task IDs across chats. A limit of N tasks counts distinct tasks started under that grant, including blocked ones, unless the user explicitly limits completions instead. Resuming the same ID does not count twice: exhausted admission capacity prevents starting another item, not finishing an already admitted one. Carry time limits as their original deadline, not a fresh duration per chat; expiry stops work, including resumption. A bare continuation does not renew limits. A session-only pause can sit inside a larger grant; a later narrower grant supersedes the broader one.

Reconcile the recorded current task, including blocked/done state, before selecting another. Recheck a saved blocker and stale verification against current files. Under one-task scope, a bare continuation stays with that task; do not skip to a queued neighbour. A broader explicit grant may select independent work only according to its mode. Retain task IDs; assign a unique project-local ID to a new task.

Before automatic selection, check ID/dependency consistency and the relevant phase boundaries. Unknown dependencies, duplicate/ambiguous IDs, cycles or contradictory ordering require plan correction; do not invent a resolution or change priorities to bypass them. A task is available only when sufficiently defined, all dependencies are genuinely done, its phase is open, and its work is authorized. Resolve material ambiguity before dependent implementation.

| Mode | Selection |
| --- | --- |
| `backlog` | First available task by declared priority, then original list order for ties or no priority. Blocked items may be skipped only within the grant. |
| `sequential` | Ordered phases, and listed order within the current phase. Never skip a blocked mandatory item to run a later item or phase. |
| `hybrid` | Ordered phases; backlog selection only inside the current phase. Independent work there may continue despite a local blocker; later phases remain closed. |

Complete a phase only when its mandatory tasks and separate exit criteria are actually satisfied. Optional remainder does not block completion. A human approval gate needs the human decision, not an agent's mark. Reconcile a gate before advancing even when every task says done. A phase-scoped grant ends at that named phase; it never expands to the next one just because the phase closed.

Carry forward explicit human decisions only within their unchanged scope; saved notes cannot grant new external permissions or override current instructions. A request to continue does not authorize publication, spending, production actions, access changes or unrelated work.

Complete authorized local preparation before presenting an external-action gate. Preserve the partial result and keep the task blocked until its remaining required steps are authorized and verified.

## Execute and check

Check files and Git/dirty state; preserve unrelated user edits and stop if ownership is unresolved. Admit the selected task within the grant, set it active and choose a proportionate approach. Handle ordinary work yourself. Use relevant skills and existing tools; extra roles, documents and handoffs are not a default. Bounded delegation remains parent-owned with explicit result and file ownership; simultaneous writers need isolation or disjoint files. Add independent evaluation when material risk or an insufficient objective check requires it.

Verify the task's actual done criteria with available project commands or a defensible focused check. Do not invent a missing command, install tooling, claim an unrun check passed, or substitute unit tests for a separately required acceptance check. Rerun affected checks after relevant changes; avoid repeating sufficient passing checks without new evidence. Source changes after verification invalidate the affected evidence.

## Save and continue

Update `work.md` at meaningful transitions, not every tool call. Keep one current status per item and a compact continuation record: mode/current phase, grant boundary and consumed limits, task ID/result/criteria, useful progress and verification, blocker and next action. Consolidate superseded agent-written notes; preserve human decisions and user-authored history. Do not rewrite or reorder the backlog, repeat every inspection, duplicate requirements, or store secrets/raw dumps. Link a detailed spec or runbook only when needed.

- On an intentional pause, preserve partial work and leave the task active with its next step; do not label it done or invent a blocker.
- On a real blocker, use blocked and name the smallest required decision/action.
- Use done only after required criteria and checks pass. Record the result, verification and remaining material limits; merge or deployment is required only if explicitly part of the task.

Treat corrections as steering while preserving useful completed work. Put adjacent ideas in queued notes without expanding the current task. When a recurring procedure warrants a project skill or an existing-skill update, suggest it briefly; do not create or change skills automatically.

After each result, re-evaluate dependency availability, phase gates and remaining authority before choosing another task. In backlog/hybrid, keep a blocked item's useful preparation and blocker while completing independent authorized work where allowed. Never mark partial work done to unlock a dependency.

Finish on scope completion, a pause, an expired deadline, exhausted capacity for another item, or no available authorized work. Distinguish a completed set from tasks still waiting on blockers or plan repair. Report results, checks and the next action; preserve enough for another chat without copying a conversation. Do not create a background scheduler or continue outside the authorized run.
