---
name: mamkin-work
description: Read or update a Mamkin 2.0 project's backlog, roadmap and decision reasons, or execute and resume its authorized work in Codex.
---

# Mamkin Work

Use `docs/mamkin/project.md` and `docs/mamkin/work.md` as entrypoints to current authoritative sources. Follow relevant links, not every project document. Reconcile saved state with current files and user instructions.

## Match the request

Distinguish an answer, a data update and execution. Answering leaves files unchanged; permission to update a plan or decision does not start its tasks. A one-off question or work outside the managed plan needs no task record. Update only material affected project facts within the request.

Keep each fact, decision and status at its existing owner; use links instead of duplicate records. Recover missing context from sources and ask only for essential missing decisions.

## Decision memory

Keep significant choices and their reasons at the existing decision source or in `project.md`. Add context, known rejected alternatives, source and revisit conditions only when useful; no mandatory ADR or empty fields.

Distinguish accepted decisions, proposals and unknowns. Do not present a suggestion as user approval; ordinary decisions within delegated scope need no new approval. When explaining why, use the recorded reason or state that it is unknown, rather than inventing one.

On an authorized revision, preserve the old choice and reason as superseded and connect them to the new choice and reason. Keep one applicable current decision. Changed facts can warrant reconsideration but do not themselves approve a replacement.

Use relevant current decisions when selecting or resuming work. Do not reopen a rejected option without a new basis. Consolidate stale agent notes while preserving human decisions, reasons and user history; avoid transcripts and secrets.

## Select authorized work

For execution in the managed plan, default to one task and backlog ordering. A mode or task list grants no whole-queue run. Resolve the current request and unchanged grant: one task, a named phase or a defined queue.

Reconcile the current task and blocker before selecting another. One-task continuation stays with that task, including blocked/done state. Retain IDs; assign a unique project-local ID when admitting a task without one, including an existing task. Do not reformat the whole backlog.

Available work has a sufficiently defined outcome and done criteria, completed dependencies, an open phase and authorization. Preserve declared priorities, dependencies and order. Unknown dependencies, duplicate IDs, cycles or contradictory ordering require plan correction, not an invented bypass.

| Mode | Selection |
| --- | --- |
| `backlog` | First available by priority, then original order for ties or no priority; skip blocked items only within the grant. |
| `sequential` | Ordered phases and listed tasks within the current phase; never skip a blocked mandatory item. |
| `hybrid` | Ordered phases; backlog selection only inside the current phase. |

Close a phase only after mandatory tasks and separate exit criteria pass. Optional remainder does not block closure. Recheck gates even if all tasks say done; human approval requires the human decision. A named-phase grant ends there after closure. Briefly explain the material reason for the selected next work.

Carry grants and applicable limits across chats. A limit of N tasks counts distinct started IDs, including blocked ones, unless the user counts completions. Resuming an admitted ID consumes no new slot; exhausted admission capacity prevents another ID, not finishing that task. Preserve the original deadline; expiry stops even resumption. Bare continuation renews neither scope nor limits. A session pause may sit inside a broader grant; a newer narrower instruction supersedes it. Detailed counters are needed only for an applicable limit.

## Keep state current

Use ordinary Codex capabilities and the project's requirements for execution and verification. Set admitted work active. Record done only after actual criteria and required checks pass; changed results invalidate affected evidence. Merge/deployment is required only when part of the task.

An intentional pause preserves partial work, active status and next step. A real blocker records the required decision/action. Retain authorized preparation before an unavailable check or unauthorized action; run scope grants no new external permissions. Partial work never unlocks dependencies.

Update the authoritative record at meaningful transitions: current task/phase, applicable grant/limits, useful progress, actual verification, blocker and next action. Preserve useful work during corrections; queue adjacent ideas without expanding the task.

After each result, reassess dependencies, phase gates and authority. Backlog/hybrid may continue independent authorized work while retaining blocked preparation. Stop at completion, pause, deadline, exhausted admission capacity or no available authorized work. Distinguish completion from waiting/plan repair and report the result and next step.
