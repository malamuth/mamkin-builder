---
name: mamkin-setup
description: Set up or reconcile minimal Mamkin 2.0 project context in Codex when the user asks to enable it.
---

# Mamkin Setup

Leave enough project context to start one task and continue in another chat. Setup ends with context and work records; it does not start product implementation.

Read the target project's instructions, Git/dirty state and only the sources needed to understand its goal, constraints and real check commands. Preserve user files and decisions. Link existing authoritative material instead of moving or duplicating it. Ask only for missing decisions that prevent useful setup; an unknown command can remain explicitly unknown.

## Minimal project records

Create or reconcile these files, using concise prose or a small table:

- `docs/mamkin/project.md`: goal, material constraints, useful source links, and durable decisions with their reasons. Existing product docs remain authoritative through links.
- `docs/mamkin/work.md`: the current task's ID, intended outcome, done criteria and status. Include the authorized scope of continuation; default to one task. Record progress, blockers and the next action only when relevant. Unscoped ideas can remain queued.
- `AGENTS.md`: retain existing content and add only missing project commands and brief links to the two records and `$mamkin-work`. Create a short file if none exists. Keep commands at their existing authoritative location when already documented; use a link rather than a second command list.

Statuses are `queued`, `active`, `blocked`, `done`. A blocked task names the missing decision/action; a completed task names its result and actual verification. A task need not have a separate specification or walkthrough. If no task is known, record that clearly rather than inventing product work.

On a repeat setup with no new facts, leave suitable files unchanged. Reconcile only missing or contradicted facts; preserve task IDs, progress, history and permission limits. Do not reset work to queued, rewrite a backlog or add duplicate instruction sections.

## Boundaries and finish

Use only the two Mamkin 2.0 skill directories in the target; no legacy Mamkin manuals, roles, metadata, presets, hooks or runtime are required. Preserve stronger project and runtime restrictions. Do not change remotes, providers, access settings or user-level configuration, install tooling, or infer external-action authority from setup.

Report where context and current work live, unresolved facts, and the next useful action. Unknown setup/run/check commands remain visible. Stop before executing the first task unless the user separately requested that work.
