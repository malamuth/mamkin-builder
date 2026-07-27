---
name: mamkin-project-evolution-audit
description: Audit a mature Mamkin project after one or more template/process updates and recommend only evidence-backed, net-positive project-process improvements. Use after major Mamkin syncs, when newer hooks, validation, model routing, subagent mechanics, or recovery tooling may be absent, or when recurring project-specific coordination friction suggests the current process should evolve.
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

4. Inspect only evidence needed to judge candidates: project brief, decision log, follow-ups, relevant custom skills/hooks/config, validation commands, and bounded Git history.
5. Apply the protocol's evidence and net-benefit gates. Absence alone is not a recommendation.
6. Render `docs/process/handoff-packets/project-evolution-audit.md` in the response. Do not create a report file.

## Boundaries

- Keep template sync and project evolution separate: sync transfers process files; this skill judges project-specific value.
- A dirty or unverified template may inform the audit, but any proposed sync must wait for a committed, clean, verified source.
- Never edit, install, enable hooks, change models, create external resources, commit, or push during the audit.
- Preserve project-specific skills, commands, human gates, and process adaptations.
- Recommend at most five `Adopt now` items, ordered by expected net value.
- Put uncertain but reversible ideas under `Bounded experiments`; explicitly reject low-value novelty.
