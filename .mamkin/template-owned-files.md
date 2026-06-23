# Mamkin Template Ownership

Use this manifest when syncing a copied project with a newer `mamkin-builder` template. The goal is to update reusable Mamkin process files without overwriting project/product data.

## Ownership Classes

### Template-Owned By Default

These files are reusable workflow surface. They may usually be updated from the upstream template after reviewing diffs:

- `.agents/skills/mamkin-*/SKILL.md`
- `.codex/agents/mamkin-*.toml`
- `.codex/hooks.json`
- `.codex/hooks/*.py`
- `.codex/rules/mamkin.rules`
- `docs/process/handoff-packets.md`
- `docs/process/handoff-packets/*.md`
- `docs/process/roles/*.md`
- `docs/process/context-health-audit.md`
- `docs/process/template-sync.md`
- `docs/templates/*.md`
- `features/README.md`

### Mixed Ownership

These files contain both reusable process and project-local adaptations. Never overwrite them blindly:

- `AGENTS.md`
- `README.md`
- `.codex/config.toml`
- `docs/process/agent-orchestration.md`
- `docs/process/init-agent.md`
- `docs/process/naming-conventions.md`
- `.mamkin/template-version.json`
- `.mamkin/template-owned-files.md`

When syncing mixed files, preserve project-specific commands, project prefix, approved MCP/runtime config, human gates, project repo/remotes, and any intentional project-specific process additions.

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
