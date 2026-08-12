---
name: mamkin-project-evolution-audit
description: Audit mature Mamkin projects for evidence-backed, net-positive process evolution. Use after major syncs, recurring workflow friction, or project-native learning that may justify a check, skill update, consolidation, or upstream proposal.
---

# Mamkin Project Evolution Audit

Run a read-only capability and profitability audit. Do not sync or apply changes.

## Workflow

1. Read `AGENTS.md` and `docs/process/project-evolution-audit.md`.
2. Verify project and template repo state. Preserve dirty worktrees.
3. Run the current template's inventory script:

   ```bash
   python3 <template>/scripts/audit_mamkin_evolution.py \
     --project <project> \
     --template <template> \
     --format json
   ```

4. Inspect only evidence needed to judge candidates: current project sources, repeated artifacts, custom mechanics, validation, and bounded history.
5. Apply the protocol's evidence, action-ladder, and net-benefit gates. Absence or a log entry alone is not a recommendation.
6. Render `docs/process/handoff-packets/project-evolution-audit.md` in the response. Do not create a report file.

## Boundaries

- Keep template sync separate: sync transfers files; this skill judges project value.
- A dirty or unverified template may inform the audit, but any proposed sync must wait for a committed, clean, verified source.
- Never edit, install, enable hooks, change models, create external resources, commit, or push during the audit.
- Treat `Propose upstream` as a handoff-only result. Never edit or commit the template repository from a copied-project task.
- Approval of an audit recommendation does not authorize cross-repository implementation. Require a separate human-approved `mamkin-builder` task. Task creation authorizes reassessment only unless its starter scope explicitly authorizes implementation.
- Never create or update a project skill during the audit. Recommend an exact candidate first; after human approval, use `skill-creator` in a separate implementation step.
- Preserve project adaptations and gates.
- Recommend at most five `Adopt now` items. Put reversible uncertainty under `Bounded experiments`; reject low-value novelty.
