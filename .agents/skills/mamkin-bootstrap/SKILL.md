---
name: mamkin-bootstrap
description: Install and adopt Mamkin Builder into a project from any machine. Use when the current project has no Mamkin skills or metadata, when `$mamkin-adopt` is unavailable, or when Codex must acquire a verified Mamkin source from GitHub before brownfield adoption. Use `mamkin-adopt` after the project-local process layer exists.
---

# Mamkin Bootstrap

Bootstrap Mamkin from outside the target repository. Do not copy this skill into the target manually; adoption installs the complete project-local process layer.

## Workflow

1. Treat the current Git root as the target. Run `pwd`, `git status --short --branch`, `git rev-parse --show-toplevel`, `git rev-parse HEAD`, and `git remote -v`. Review may inspect a dirty target, but never apply or mutate it until it is clean.
2. If valid `.mamkin/template-version.json` says `initializedProject: true`, stop bootstrap and route to the project's `mamkin-template-sync` skill.
3. Acquire the Mamkin source:
   - Prefer a human-named local checkout only when it is clean and `HEAD` equals `origin/main`.
   - Otherwise ask before network access, create a dedicated temporary directory with `mktemp -d`, and clone `https://github.com/malamuth/mamkin-builder.git` into it.
4. Verify the source with `git status --short --branch`, `git rev-parse HEAD`, and `git rev-parse origin/main`. Never use an uncommitted or mismatched source for apply.
5. Read the acquired source's `.agents/skills/mamkin-adopt/SKILL.md` and `docs/process/adopt-existing-project.md` completely.
6. Run its `scripts/adopt_mamkin_process.py` in review mode against the target. Present the classification, both commits, clean states, plan digest, collisions, manual reconciliation, and human gates.
7. Apply nothing until the human approves that exact plan. After approval, run apply with the expected source commit, target commit, and plan digest.
8. Continue the acquired adoption protocol through project reconciliation, baseline validation, self-review, and the adoption handoff. Do not stop after seeding files.
9. Remove only a temporary checkout created by this run, using its exact path, after adoption evidence no longer depends on it. Preserve a human-provided checkout.

## Boundaries

- Network clone, Git initialization, external writes, providers, secrets, production actions, and destructive changes retain their normal human gates.
- Do not install a lone project-local skill, overwrite existing target paths, or implement product features during bootstrap.
- A source or target change invalidates the reviewed plan; re-review instead of reusing its digest.
