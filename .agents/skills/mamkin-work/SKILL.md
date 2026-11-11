---
name: mamkin-work
description: Execute or resume authorized Mamkin 2.0 tasks in Codex using a backlog or ordered stages, preserving progress across chats.
---

# Mamkin Work

Use `docs/mamkin/project.md` and `docs/mamkin/work.md` as entrypoints to current authoritative sources. Recover missing context from those sources; ask for essential missing decisions.

## Choose and reconcile

Default to one task and backlog ordering. Scheduling mode never grants continuation: resolve the current request and unchanged explicit grant for one task, a named phase or a defined queue. Preserve priorities, dependencies, phase order and exit criteria.

Carry limits and admitted IDs across chats. A limit of N tasks counts distinct tasks started, including blocked ones, unless the user explicitly counts completions. Resuming an admitted ID consumes no new slot; exhausted admission capacity prevents another ID, not finishing that task. Preserve the original deadline; expiry stops even resumption. Bare continuation renews neither limits nor scope. A session pause may sit inside a larger grant; a later narrower grant supersedes it.

Reconcile the current task, blocker and verification against actual files before selecting another. One-task continuation stays with that ID, including blocked/done state; a broader grant may select independent work by mode. Retain IDs; assign new tasks unique project-local IDs.

Before selection, check IDs, dependencies and phase boundaries. Unknown dependencies, duplicate/ambiguous IDs, cycles or contradictory ordering require plan correction. Do not invent resolutions or reorder the plan. Available work has a sufficiently defined outcome, genuinely completed dependencies, an open phase and authorization. Resolve material ambiguity before dependent implementation.

| Mode | Selection |
| --- | --- |
| `backlog` | First available task by declared priority, then original list order for ties or no priority. Blocked items may be skipped only within the grant. |
| `sequential` | Ordered phases, and listed order within the current phase. Never skip a blocked mandatory item to run a later item or phase. |
| `hybrid` | Ordered phases; backlog selection only inside the current phase. Independent work there may continue despite a local blocker; later phases remain closed. |

Close a phase only when mandatory tasks and separate exit criteria are satisfied. Optional remainder does not block closure. Recheck exit gates even when all tasks say done; human approval requires the human decision. A named-phase grant ends there, even after closure.

Saved decisions apply only within unchanged scope. Continuation grants no new publication, spending, production, access or unrelated authority. Complete authorized local preparation before an external-action gate; preserve it and keep the task blocked until remaining required steps are authorized and verified.

## Execute and check

Inspect Git/dirty state; preserve user edits and resolve ownership conflicts. Admit the selected task within the grant and set it active. Handle ordinary work directly with relevant skills/tools. For useful bounded delegation, specify result, ownership, sources and verification; the parent owns integration. Concurrent writers need isolation or disjoint files. Require a different agent/human's evaluation when material risk or insufficient objective checks demand it; missing required evaluation prevents done.

Verify actual done criteria with project commands or a defensible focused check. Do not invent commands, install missing tooling, claim unrun checks or replace required acceptance with unit tests. Source changes invalidate affected evidence; repeat affected checks, not already sufficient unaffected ones.

## Save and continue

Update the authoritative work record at meaningful transitions. Keep one current status per item and compact continuation context: mode/phase, grant/consumed limits, ID/outcome/criteria, progress/checks, blocker and next action. Consolidate stale agent notes while preserving human decisions and user history. Link detailed requirements only when needed; avoid duplicate requirements, inspection logs and secrets.

- Intentional pause: preserve partial work, active status and next step.
- Blocker: use blocked with the required decision/action.
- Done: all required criteria/checks passed; record result, verification and material limits. Merge/deployment belongs to done only when explicitly required.

Apply current user corrections while preserving useful work. Queue adjacent ideas without expanding the task. For recurring project procedures, include a concrete reuse proposal at handoff: prefer updating an existing matching skill; otherwise suggest a project skill. Name observed repetition, trigger and saved work. This advice never blocks current work or authorizes skill creation/changes.

After each result, reassess dependencies, phase gates and remaining authority. Backlog/hybrid may continue independent authorized work while retaining blocked preparation; partial work never unlocks dependencies. Stop at completion, pause, deadline, exhausted admission capacity or no available authorized work. Distinguish completion from blockers/plan repair and report checks and next action. No background scheduler.
