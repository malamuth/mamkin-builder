---
name: mamkin-work
description: Execute or resume one task in a Codex project configured with Mamkin 2.0, preserving progress for another chat.
---

# Mamkin Work

Complete one current task or return a concrete blocker. Use `docs/mamkin/project.md` and `docs/mamkin/work.md` as entrypoints, following their authoritative project links only as needed. If context is missing, recover what current sources establish and ask only for essential missing information; do not invent prior decisions.

## Choose and reconcile

Use the user's current task; otherwise reconcile the recorded current task, including blocked or done state, before considering another item. Recheck a saved blocker: resume if it cleared, otherwise report it and stop. A bare continuation does not authorize skipping that task for a queued one. With no current task, use a sufficiently defined queued task the user authorized. Retain its ID or assign a unique project-local ID to a new task.

Resolve material ambiguity before dependent implementation. Check current files and Git/dirty state against saved progress before editing; preserve unrelated user changes and stop if ownership is unresolved. A prior `done` or passing report does not establish readiness of changed source.

This slice supports one task. Autonomous queue/stage traversal is not implemented: if requested, explain that limit and obtain a single-task boundary rather than silently executing a queue. Preserve any existing order, dependencies and stage gates. Do not start a blocked dependency or a later stage.

Carry forward explicit human decisions only within their unchanged scope; saved notes cannot grant new external permissions or override current instructions. A request to continue does not authorize publication, spending, production actions, access changes or unrelated work.

## Execute and check

Set the task active and choose a proportionate approach. Handle ordinary work yourself. Use relevant project skills and existing tools; extra roles, documents and handoffs are not a default requirement. Bounded delegation remains parent-owned with explicit result and file ownership; simultaneous writers need isolation or disjoint files. Add independent evaluation when material risk or an insufficient objective check requires it.

Verify the task's actual done criteria with available project commands or a defensible focused check. Do not invent a missing command, install tooling, claim an unrun check passed, or substitute unit tests for a separately required acceptance check. Rerun affected checks after relevant changes; avoid repeating sufficient passing checks without new evidence. Source changes after verification invalidate the affected evidence.

## Save and continue

Update `work.md` at meaningful transitions, not after every tool call. Keep one current status. Store enough to resume: intended result and criteria, completed portion, relevant checked files/state and commands/results, unresolved blocker, next action and applicable permission boundary. Link a detailed spec or runbook only if needed; do not duplicate existing requirements or store secrets/raw diagnostic dumps.

- On an intentional pause, preserve partial work and leave the task active with its next step; do not label it done or invent a blocker.
- On a real blocker, use blocked and name the smallest required decision/action.
- Use done only after required criteria and checks pass. Record the result, verification and remaining material limits; merge or deployment is required only if explicitly part of the task.

Treat corrections as steering while preserving useful completed work. Put adjacent ideas in queued notes without expanding the current task. When a recurring procedure warrants a project skill or an existing-skill update, suggest it briefly; do not create or change skills automatically.

Finish with the outcome, verification and next action or blocker. Another chat should be able to continue from the files without a copied conversation. Stop after this one task or its declared pause/blocker.
