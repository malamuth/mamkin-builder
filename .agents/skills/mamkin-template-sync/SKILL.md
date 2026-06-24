---
name: mamkin-template-sync
description: Compare and update a copied project's Mamkin process layer from the current mamkin-builder template while preserving project-owned data.
---

# Mamkin Template Sync

Use this skill when a copied project should align its Mamkin process files with the latest template version from GitHub or a local template checkout.

## Workflow

1. Read `AGENTS.md`.
2. Read `docs/process/template-sync.md`.
3. Read `.mamkin/template-version.json` and `.mamkin/template-owned-files.md` when present.
4. Check repo state with `pwd`, `git status --short --branch`, `git rev-parse HEAD`, and `git remote -v`.
5. Locate the target upstream template:
   - Prefer a verified local path when available: it must be clean and its HEAD must match `origin/main`, unless the human explicitly approves a local-only state.
   - Otherwise use `https://github.com/malamuth/mamkin-builder.git` after asking for network approval if the environment requires it.
6. For a local upstream checkout, run `git status --short --branch`, `git rev-parse HEAD`, and `git rev-parse origin/main` in that checkout and report the result.
7. Run review mode first. Classify changes as template-owned, mixed, project-owned, or never-sync.
8. Apply changes only after the human approves the patch plan or explicitly requested apply mode.
9. After applying, update `.mamkin/template-version.json`, run `git diff --check`, and return the sync packet from `docs/process/template-sync.md`.

## Boundaries

- Never overwrite project-owned files from the template.
- Never sync `.git`, remotes, secrets, private URLs, provider keys, production data, or machine-local state.
- Mixed files require merge review and preservation notes.
- Do not call a local checkout "latest GitHub" unless it is clean and HEAD matches `origin/main`, or the human explicitly approves local-only template state.
- If template metadata is missing or `TBD`, use heuristic first-sync review mode and ask before applying mixed-file changes.
- This skill updates the Mamkin process layer only; it does not implement product features.
