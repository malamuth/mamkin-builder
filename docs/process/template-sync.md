# Mamkin Template Sync

Use this protocol to align a copied project's Mamkin process layer with a newer `mamkin-builder` template while preserving project/product data.

This is a process sync, not a product migration. It must not overwrite project plans, feature specs, code, secrets, remotes, or deployment config.

## Inputs

- Current copied project worktree.
- Upstream template source, preferably `https://github.com/malamuth/mamkin-builder.git` or a verified local clone/path.
- `.mamkin/template-version.json`, if present.
- `.mamkin/template-owned-files.md`, if present.

If the copied project lacks `.mamkin/` metadata, run in first-sync review mode and create the metadata only after human approval.

## Upstream Verification

When using a local `mamkin-builder` checkout as the upstream template, verify it before comparing:

```bash
git status --short --branch
git rev-parse HEAD
git rev-parse origin/main
```

A local checkout is acceptable as the upstream source only when it is clean and its HEAD matches `origin/main`. If the local checkout has uncommitted changes, is ahead/behind, or points at a commit that does not match `origin/main`, do not treat it as latest GitHub state unless the human explicitly approves using that local-only state. Otherwise fetch/clone the GitHub upstream when network access is available, or return a blocked/review-only packet that names the verification gap.

## Ownership

Use `.mamkin/template-owned-files.md` as the source of truth for file classes:

- Template-owned files can usually be updated from upstream after diff review.
- Mixed files require merge review and preservation notes.
- Project-owned files are protected.
- Never sync secrets, `.git`, remotes, provider credentials, production data, or machine-local state from the template.

## Sync Modes

### Review Mode

Default mode. Produce a report only:

- Current project HEAD and dirty state.
- Current recorded template commit and last sync commit.
- Upstream template commit inspected.
- Template-owned file diffs.
- Mixed-file diffs and merge risks.
- Project-owned files that would be protected.
- Recommended patch plan.

### Apply Mode

Only run apply mode after the human approves the patch plan. Apply:

- Template-owned changes that are safe and process-only.
- Mixed-file merges where project-specific data is preserved.
- Metadata update in `.mamkin/template-version.json`.

After applying, run `git diff --check` and report remaining manual review items.

## Baseline Strategy

If `lastProcessSyncCommit` is known, prefer a three-way review:

```text
base: upstream template at lastProcessSyncCommit
ours: copied project
theirs: upstream template at target commit
```

If the baseline is unknown or `TBD`, use two-way review and require extra human confirmation for mixed files.

## Safe Merge Rules

Preserve:

- Project name, prefix, README product description, commands, human gates, and approved MCP/runtime config.
- Project decisions, roadmap, feature specs, follow-ups, walkthroughs, and product docs.
- Project repo/remotes and GitHub setup decisions.
- Custom project skills, custom role cards, and non-`mamkin-*` agent presets unless explicitly template-derived.

Update:

- Reusable Mamkin skills.
- Generic process docs and handoff packet templates.
- Generic hooks/rules/presets when they remain project-safe.
- Template ownership/version metadata.

Ask before:

- Changing `.codex/config.toml` runtime, sandbox, hooks, inherited env, MCP servers, or external connectors.
- Replacing mixed files with large edits.
- Removing project-local customizations.
- Running networked fetch/clone when network access is not already available.

## Output Packet

Return this packet:

```text
Status: review only | applied | blocked
Worktree:
Branch:
HEAD:
Dirty state:
Current template commit:
Current last sync commit:
Target upstream:
Target upstream commit:
Upstream verification:
Ownership manifest used:
Template-owned changes:
Mixed-file changes:
Project-owned files protected:
Applied changes:
Metadata update:
Checks run:
Human decisions needed:
Recommended next action:
```
