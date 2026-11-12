# Mamkin 2.0

A thin project-memory layer for Codex: backlog, roadmap and decisions with their reasons, stored in Markdown. Mamkin helps select and resume authorized work across chats. Ordinary Codex handles implementation and verification under the project's rules.

Mamkin 2.0 is the primary version on `main`. The product consists of two skills; no Mamkin role system, custom runtime or mandatory audit/rollover workflow is required.

## Start using Mamkin 2.0

For a project without Mamkin 1.x, copy only these two directories into its `.agents/skills/`, preserving existing files:

- [`mamkin-setup`](.agents/skills/mamkin-setup/SKILL.md)
- [`mamkin-work`](.agents/skills/mamkin-work/SKILL.md)

Then ask Codex in that project:

```text
Use $mamkin-setup to set up project memory. Preserve existing context,
backlog, roadmap and decision sources; link them instead of duplicating them.
Do not start implementation.
```

Setup prepares concise `docs/mamkin/project.md` and `docs/mamkin/work.md` entrypoints and adds missing navigation to the project's `AGENTS.md`. Existing plans and ADRs can remain the owners of their data. Setup does not authorize execution.

Use `$mamkin-work` to inspect or update the plan, explain decisions, or execute a specifically authorized task or phase. For example:

```text
Use $mamkin-work to explain the current roadmap, what is available next
and why. Do not change files or start tasks.
```

Backlog, sequential phases and a combination of both are supported. Planning mode does not grant permission to run the queue. When continuing in a new chat, read the project entrypoints and reconcile saved state with the current files and request.

## Migrate an existing Mamkin 1.x project

Use the separate [one-time migration procedure](docs/process/mamkin-1-to-2-migration.md) in the target project's own chat. It preserves project data, decision reasons, unfinished work and real safeguards, removes confirmed obsolete process, and prepares a fresh coordinator. This procedure has been reviewed but has not yet been exercised on a real project.

Do not install 2.0 over an active 1.x setup by copying the whole repository or running the old bootstrap/init/adopt/template-sync flows.

## Scope and evidence

The [v0.3 specification](docs/project/mamkin-2-spec.md) and [MVP plan](docs/project/mamkin-2-mvp-plan.md) define the contract. The [functional checks](docs/follow-ups/mamkin-2-v03/README.md) retain failures and limitations alongside the final assessment. The [earlier comparison](docs/follow-ups/mamkin-2-stage-3/README.md) found no advantage over ordinary Codex on seven simple tasks. A comparison with identical Markdown data and the real-project pilot remain outstanding; publication as the primary version does not mean MVP acceptance or proven efficiency gains.

## Repository contents

This is the development repository, not a project template to copy wholesale. Only the two skill directories above are the Mamkin 2.0 installation payload. Specifications, eval tools and saved results support development and do not belong in target projects.

Legacy Mamkin 1.x process files, skills and Codex configuration remain here as development/migration sources. They are not part of the 2.0 installation. The repository's own agent/runtime configuration is not a target-project configuration. Historical [1.x documentation](https://github.com/malamuth/mamkin-builder/blob/6a5c99d38043955e2b966f22922009efed68b62b/README.md) remains available at its last main commit.
