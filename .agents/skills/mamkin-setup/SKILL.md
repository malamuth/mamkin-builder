---
name: mamkin-setup
description: Set up or reconcile minimal Mamkin 2.0 backlog, roadmap and decision-memory entrypoints in a Codex project.
---

# Mamkin Setup

Find existing owners of project context, tasks, phases and decisions. Read project instructions, Git/dirty state and only needed sources. Preserve user changes, IDs, progress, decision reasons and history. Unknown commands or reasons stay unknown; ask only for decisions preventing useful setup.

Create or reconcile concise entrypoints:

- `docs/mamkin/project.md`: goal, material constraints, source links and significant decisions with reasons. Link existing decision/ADR sources rather than copying or moving them. Distinguish accepted choices, proposals and unknowns; retain relevant superseded reasons and links to current choices.
- `docs/mamkin/work.md`: backlog/roadmap and current work, or links to their existing owner. Tasks have IDs, outcomes, done criteria and queued/active/blocked/done state; ideas may stay brief until refined. Preserve priorities, dependencies and order. Keep phase goals, mandatory/optional work and exit criteria when used. Default to backlog absent declared sequencing.
- `AGENTS.md`: preserve content; add only missing short links to context/work and `$mamkin-work`. Link existing commands instead of repeating them.

Keep planning mode separate from execution authority. Preserve applicable grants, consumed limits, deadlines and useful continuation state. Setup or choosing a mode grants no execution.

With no new facts, leave suitable files unchanged. Reconcile missing/contradicted facts without resetting progress, erasing reasons, reordering work or duplicating sources. No new decision registry, required ADR format or runtime is needed; only these two Mamkin skill directories are required.

Report locations, unresolved material facts and next useful action. Setup neither starts implementation unless separately requested, nor authorizes tooling installation or external/configuration changes. Existing project/runtime restrictions remain authoritative.
