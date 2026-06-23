# Naming Conventions

Use this file when creating durable docs or separate agent threads.

Project prefix: TBD

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

For the main coordinator thread, use:

```text
👑 <project-prefix> Coordinator - project coordination
```

For an outgoing/replaced coordinator thread, rename or archive it when the platform supports that:

```text
👑 <project-prefix> Coordinator - archived <short-reason>
```

If the platform requires creating the fresh coordinator before the old coordinator can be archived, the fresh coordinator may temporarily use:

```text
👑 <project-prefix> Coordinator - reset baseline
```

After the reset prompt is delivered and the old coordinator is archived/renamed, promote the fresh coordinator to the main coordinator title.

Examples:

- `👑 <project-prefix> Coordinator - project coordination`
- `<project-prefix> C01 Architect - first smoke slice`
- `<project-prefix> F01 Implementation - task list API`
- `<project-prefix> F01 Walkthrough - acceptance pass`
- `<project-prefix> F01 Reviewer - persistence and tests`

Rules:

- During init or coordinator kickoff, replace `Project prefix: TBD` with one short project prefix. Do not append a second prefix rule or keep stale project examples.
- When init continues in the same thread as coordinator, rename that thread to the coordinator pattern before the first coordinator action.
- After coordinator rollover, the fresh coordinator should use the main coordinator title; the old coordinator should be archived or renamed with the archived pattern when tooling supports it.
- Do not leave two unarchived coordinator threads with titles that both read as active. If cleanup tooling is unavailable, the outgoing coordinator must say so in its final response and stop coordinating.
- Coordinator prompts for separate worker threads must include the exact `Thread name:`. If the created thread title differs, rename it or request rename before continuing.
- Use `C##` for roadmap candidates and `F##` for feature specs.
- Use role names from `docs/process/roles/`: `Analyst`, `Architect`, `Implementation`, `Reviewer`, `Walkthrough`, `Deployment`, `UX`, or an initialized custom role display name.
- Keep short scope human-readable and kebab-free enough to scan in thread lists.
- Do not include status in thread names; status changes too often and is easy to leave stale.
- Put status in worker prompts, packets, and coordinator notes instead.
- Include exact worktree, branch, and commit in the worker prompt and packet, not in the thread title.
