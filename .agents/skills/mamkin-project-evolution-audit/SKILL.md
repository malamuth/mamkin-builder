---
name: mamkin-project-evolution-audit
description: Audit a mature Mamkin project and recommend evidence-backed, net-positive evolution from template capabilities and project-native learning. Use after major Mamkin syncs; when newer process mechanics may be absent; or when decision logs, surprise logs, follow-ups, repeated artifacts, or project-specific skills suggest a reusable check, reference, skill update, new skill, consolidation, or upstream improvement.
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

4. Inspect only evidence needed to judge candidates: project brief, decision and learning logs, follow-ups, repeated artifacts, relevant custom skills/hooks/config, validation commands, and bounded Git history.
5. Apply the protocol's evidence, action-ladder, and net-benefit gates. Absence or a log entry alone is not a recommendation.
6. Render `docs/process/handoff-packets/project-evolution-audit.md` in the response. Do not create a report file.

## Boundaries

- Keep template sync separate: sync transfers files; this skill judges project value.
- A dirty or unverified template may inform the audit, but any proposed sync must wait for a committed, clean, verified source.
- Never edit, install, enable hooks, change models, create external resources, commit, or push during the audit.
- Never create or update a project skill during the audit. Recommend an exact candidate first; after human approval, use `skill-creator` in a separate implementation step.
- Preserve project skills, commands, human gates, and adaptations.
- Recommend at most five `Adopt now` items, ordered by expected net value.
- Put uncertain but reversible ideas under `Bounded experiments`; explicitly reject low-value novelty.
