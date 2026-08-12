---
name: mamkin-adopt
description: Adopt Mamkin Builder into an existing project that was created without Mamkin. Use for brownfield repository audits, safe process-layer bootstrap, project-context reconstruction, ownership reconciliation, baseline validation, and coordinator handoff. Do not use for a new copied template or a project with valid Mamkin metadata.
---

# Mamkin Adopt

Use this skill when an existing repository should gain the Mamkin workflow without replacing its product code, Git history, remotes, deployment state, or project-specific instructions.

## Workflow

1. Read `AGENTS.md` and `docs/process/adopt-existing-project.md`.
2. Classify the repository before editing. Route new copied templates to `mamkin-init` and initialized Mamkin projects to `mamkin-template-sync`.
3. Run the required Git preflight and a read-only inventory. Treat current project sources as authoritative and inspect environment-variable names only.
4. Run the focused brownfield interview only for facts the repository does not establish.
5. Use `scripts/adopt_mamkin_process.py` in review mode to produce the pinned adoption plan.
6. Apply no files until the human approves that exact plan. Re-review when the source commit, target commit, dirty state, or plan digest changes.
7. After approval, seed collision-free process files, reconcile mixed files manually, and create project-owned docs from current evidence rather than template placeholders.
8. Run safe existing checks, complete the adoption self-review, and return `docs/process/handoff-packets/adoption.md`.

## Boundaries

- Never overwrite an existing target file automatically.
- Never copy product code, tests, migrations, secrets, remotes, provider state, production data, or deployment configuration from the template.
- Do not invent setup, run, validation, architecture, or recovery facts.
- Keep external actions and production changes behind the human gates in `AGENTS.md`.
- Adoption installs process only; it does not implement the upcoming product change.
