# Naming Conventions

Use this file when creating durable docs or separate agent threads.

## Doc Naming

Use predictable kebab-case names for docs produced by agents:

- Roadmap: `features/00-roadmap.md`.
- Feature specs: `features/NN-short-kebab-title.md`, where `NN` is the zero-padded implementation order.
- Walkthroughs/runbooks: `docs/walkthroughs/feature-NN-short-kebab-title.md`.
- Follow-ups: `docs/follow-ups/feature-NN-short-kebab-title.md`; add a date suffix only when multiple follow-up notes are needed for the same feature.
- Durable project decisions: append to `docs/project/decision-log.md`.
- Durable project analysis or architecture notes: place under `docs/project/` with a short kebab-case name, for example `docs/project/storage-architecture.md`.

Do not store live thread ownership, temporary branch state, secrets, tokens, or magic links in durable docs.

## Thread Naming

Use predictable names for separate agent threads:

```text
<project-prefix> <slice-id> <role> - <short-scope>
```

Examples:

- `HL C01 Architect - local smoke slice`
- `HL F01 Implementation - local list UI`
- `HL F01 Walkthrough - local acceptance`
- `HL F01 Reviewer - persistence and tests`

Rules:

- Choose a short project prefix during init or coordinator kickoff, for example `HL` for Hearthlist.
- Use `C##` for roadmap candidates and `F##` for feature specs.
- Use role names from `docs/process/roles/`: `Analyst`, `Architect`, `Implementation`, `Reviewer`, `Walkthrough`, `Deployment`, `UX`, or an initialized custom role display name.
- Keep short scope human-readable and kebab-free enough to scan in thread lists.
- Do not include status in thread names; status changes too often and is easy to leave stale.
- Put status in worker prompts, packets, and coordinator notes instead.
- Include exact worktree, branch, and commit in the worker prompt and packet, not in the thread title.
