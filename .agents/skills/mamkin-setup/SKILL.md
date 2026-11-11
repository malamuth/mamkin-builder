---
name: mamkin-setup
description: Set up or reconcile minimal Mamkin 2.0 project context in Codex when the user asks to enable it.
---

# Mamkin Setup

Leave enough project context to select authorized work and continue in another chat. Setup ends with context and work records; it does not start product implementation.

Read the target project's instructions, Git/dirty state and only the sources needed to understand its goal, constraints and real check commands. Preserve user files and decisions. Link existing authoritative material instead of moving or duplicating it. Ask only for missing decisions that prevent useful setup; an unknown command can remain explicitly unknown.

## Minimal project records

Create or reconcile these files, using concise prose or a small table:

- `docs/mamkin/project.md`: goal, material constraints, useful source links, and durable decisions with their reasons. Existing product docs remain authoritative through links.
- `docs/mamkin/work.md`: task IDs, intended outcomes, done criteria and statuses. Preserve existing order, priorities and dependencies. Record the scheduling mode: `backlog`, `sequential` or `hybrid`; absent declared sequencing, default to backlog. For ordered phases, keep their goals, mandatory/optional items, current phase and separate exit criteria. Use existing plan links rather than copying detailed requirements.
- `AGENTS.md`: retain existing content and add only missing project commands and brief links to the two records and `$mamkin-work`. Create a short file if none exists. Keep commands at their existing authoritative location when already documented; use a link rather than a second command list.

Statuses are `queued`, `active`, `blocked`, `done`. A blocked task names the missing decision/action; a completed task names its result and actual verification. A task need not have a separate specification or walkthrough. If no task is known, record that clearly rather than inventing product work.

Keep scheduling mode separate from the user's continuation grant: default one task, or an explicitly authorized named phase/queue with applicable limits. Preserve any consumed limits and deadlines. Choosing a mode during setup is not authorization to execute its tasks. Record useful progress, blockers and next action only when relevant; new unscoped ideas can remain queued outside the current grant.

On a repeat setup with no new facts, leave suitable files unchanged. Reconcile only missing or contradicted facts; preserve task IDs, progress, history and permission limits. Do not reset work to queued, rewrite a backlog or add duplicate instruction sections.

## Boundaries and finish

Use only the two Mamkin 2.0 skill directories in the target; no legacy Mamkin manuals, roles, metadata, presets, hooks or runtime are required. Preserve stronger project and runtime restrictions. Do not change remotes, providers, access settings or user-level configuration, install tooling, or infer external-action authority from setup.

Report where context and current work live, unresolved facts, and the next useful action. Unknown setup/run/check commands remain visible. Stop before executing the first task unless the user separately requested that work.
