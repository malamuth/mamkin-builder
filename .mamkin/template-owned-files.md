# Mamkin Template Ownership

Use this guide when syncing a copied project with a newer `mamkin-builder` template. The goal is to update reusable Mamkin process files without overwriting project/product data.

`.mamkin/process-manifest.json` is the machine-readable allowlist used by sync tooling. This document explains the ownership policy and should remain aligned with it.

## Ownership Classes

### Template-Owned By Default

These files are reusable workflow surface. They may usually be updated from the upstream template after reviewing diffs:

- `.agents/skills/mamkin-*/**`
- `.codex/agents/mamkin-*.toml`
- `.codex/hooks.json`
- `.codex/hooks/*.py`
- `.codex/rules/mamkin.rules`
- `.mamkin/evolution-capabilities.json`
- `.mamkin/validation-map.json`
- `docs/process/handoff-packets.md`
- `docs/process/handoff-packets/*.md`
- `docs/process/roles/*.md`
- `docs/process/context-health-audit.md`
- `docs/process/adopt-existing-project.md`
- `docs/process/execution-lane-routing.md`
- `docs/process/thread-operations.md`
- `docs/process/prompt-evals.md`
- `docs/process/project-evolution-audit.md`
- `docs/process/template-sync.md`
- `docs/templates/*.md`
- `evals/mamkin-prompt-cases.json`
- `evals/mamkin-role-model-matrix.json`
- `scripts/audit_mamkin_evolution.py`
- `scripts/adopt_mamkin_process.py`
- `scripts/plan_validation.py`
- `scripts/sync_mamkin_process.py`
- `scripts/validate_prompt_contracts.py`
- `tests/__init__.py`
- `tests/test_adopt_mamkin_process.py`
- `tests/test_audit_mamkin_evolution.py`
- `tests/test_plan_validation.py`
- `tests/test_sync_mamkin_process.py`
- `features/README.md`

### Mixed Ownership

These files contain both reusable process and project-local adaptations. Never overwrite them blindly:

- `AGENTS.md`
- `README.md`
- `.codex/config.toml`
- `docs/process/agent-orchestration.md`
- `docs/process/init-agent.md`
- `docs/process/naming-conventions.md`
- `.mamkin/process-manifest.json`
- `.mamkin/template-version.json`
- `.mamkin/template-owned-files.md`

When syncing mixed files, preserve project-specific commands, project prefix, approved MCP/runtime config, human gates, project repo/remotes, and any intentional project-specific process additions.

Treat upstream expansions of `.mamkin/process-manifest.json` as new sync authority: review and merge them explicitly before they may authorize additional template-owned paths.

### Project-Owned

These files are project/product data. Do not replace them from the template during sync:

- `docs/project/**`
- `features/00-roadmap.md`
- `features/[0-9][0-9]-*.md`
- `docs/follow-ups/**`
- `docs/walkthroughs/**`
- Product source code, tests, assets, migrations, deployment files, and stack-specific config created after init.
- Non-`mamkin-*` custom skills and agent presets unless the human explicitly says they are template-derived.

### Never Sync From Template

- `.git/**`
- Secrets, local env files, private URLs, tokens, provider keys, billing config, production data, and machine-local setup.
- Project-specific remotes, GitHub project settings, external service config, and MCP/provider credentials.

## Sync Rules

1. Run sync in review mode first.
2. Compare the copied project, the latest upstream template, and the recorded baseline commit when available.
3. Template-owned files may be updated directly only when the diff is process-only and does not remove project-approved local additions.
4. Mixed files require a merge review and a short explanation of preserved project data.
5. Project-owned files are protected by default.
6. If `templateCommit` or `lastProcessSyncCommit` is `TBD`, treat the first sync as heuristic and require human review before applying mixed-file changes.
7. After a successful sync, update `.mamkin/template-version.json` with the upstream commit used for the process sync.
