# Adopt Mamkin Into An Existing Project

Use this protocol to add the Mamkin process layer to a brownfield repository without transplanting the product into a template clone. The target repository, its current human decisions, product sources, Git history, remote, and deployment configuration remain authoritative.

## Portable Bootstrap

The target cannot discover a project-local `mamkin-adopt` skill before adoption. Do not manually copy a lone Mamkin skill into the target; that creates partial-adoption markers without the complete process layer.

On any Codex machine, install the self-contained global entrypoint from GitHub:

```text
Use $skill-installer to install:
https://github.com/malamuth/mamkin-builder/tree/main/.agents/skills/mamkin-bootstrap
```

The installed skill becomes available on the next turn. From the target project, invoke `$mamkin-bootstrap`. It acquires a verified full Mamkin source, then hands execution to this adoption protocol. The approved adoption apply installs all project-local Mamkin skills and process files together.

## Scope And Routing

Use adoption when an existing project has no valid Mamkin initialization metadata.

- New or empty project copied from this template: use `mamkin-init`.
- Valid `.mamkin/template-version.json` with `initializedProject: true`: use `mamkin-template-sync` for process updates or deliberate reinitialization when the project brief must be replaced.
- Recognizable Mamkin files but missing or invalid metadata: classify as partial adoption and review recovery; never overwrite the existing files.
- Non-Git target: continue read-only discovery, then ask before `git init`; do not apply the process layer without a stable Git baseline.
- Monorepo: adopt at the Git root unless the human approves a narrower independently operated repository boundary.

Adoption is process work. Do not implement the upcoming feature, alter production, configure providers, install dependencies, or change remotes during adoption.

## Safety And Git Preflight

Before editing, run in the target:

```bash
pwd
git status --short --branch
git rev-parse --show-toplevel
git rev-parse HEAD
git remote -v
```

Run the equivalent status and commit checks in the Mamkin source. Prefer a verified local checkout whose clean HEAD matches `origin/main`; otherwise ask before networked fetch or clone. A human may explicitly approve a named clean local-only source commit.

Review mode may inspect a dirty target but must report the dirty boundary. Automatic apply requires a clean source and target. Preserve all user changes. Re-review when the source commit, target commit, dirty state, or plan digest changes.

Inspect environment-variable names and committed configuration only. Never print, copy, or store secret values, private URLs, provider keys, production data, or machine-local state.

## Repository Classification And Inventory

Record:

- Git root, branch, HEAD, dirty state, and remotes.
- Product purpose, shipped workflows, authoritative docs, and protected behavior.
- Languages, frameworks, package managers, repository shape, and major component boundaries.
- Existing setup, run, check, test, build, migration, preview, deploy, health, and rollback commands without executing unsafe or networked commands.
- Source, tests, migrations, CI, deployment configuration, feature flags, observability, data, auth/security, public contracts, external services, and recovery controls.
- Environment-variable names and approved secret locations, never values.
- Existing agent instructions, project-local skills, hooks, rules, and runtime config.

Current repository evidence outranks generic template assumptions. If a command, deployment fact, or architecture boundary is unknown, record the gap instead of inventing it.

## Focused Brownfield Interview

Ask one to three high-leverage questions per round and reuse repository evidence. Offer a recommended choice only when a real decision exists. Close each round with decisions, assumptions, conflicts, and open questions.

1. **Current production truth:** users, valuable jobs, shipped interfaces, protected behavior, authoritative sources, and current operational state.
2. **Change intent:** upcoming milestone, smallest reversible valuable slice, non-goals, completion evidence, and compatibility requirements.
3. **Operational risk:** sensitive or hard-to-recover data, migrations, auth, privacy, external services, previews, rollback, secrets path, and human gates.
4. **Delivery model:** existing local checks, CI coverage, deployment ownership, Git practices, recommended orchestration, occasional parallel work, and genuinely recurring custom roles.

## Deterministic Adoption Review

Run from the Mamkin source or use the absolute script path:

```bash
python3 scripts/adopt_mamkin_process.py \
  --source /verified/mamkin-builder \
  --target /existing/project
```

The review reports the exact source and target commits, dirty state, repository classification, plan digest, collision-free files that may be seeded, mixed files requiring manual work, existing collisions, and project-owned placeholders that must be created from project evidence.

Brownfield ownership is conservative:

- Missing template-owned path: `seed`.
- Non-regular or symlinked template-owned source path: `blocked-source`.
- Any existing target path, even one upstream calls template-owned: `protect-existing`.
- Missing mixed path: `manual-create`.
- Existing mixed path: `manual-merge`.
- Project-owned template placeholder: `create-project-context`; never copy it.
- Never-sync or unclassified path: do not transfer.

An existing target path always outranks upstream ownership. Do not compare or read its contents merely to decide whether it is safe to overwrite.

## Human Approval And Apply

Present the exact plan and ask for approval before local writes. Approval covers only that process overlay and the named manual project-doc adaptations. Ask separately for Git initialization, remotes or pushes, provider/MCP setup, dependency installation, secrets, paid resources, production actions, DNS, public posting, destructive migrations, or production data access.

After approval, pin all reviewed evidence:

```bash
python3 scripts/adopt_mamkin_process.py \
  --source /verified/mamkin-builder \
  --target /existing/project \
  --apply \
  --expected-source-commit <source-commit> \
  --expected-target-commit <target-commit> \
  --expected-plan-digest <plan-digest>
```

Apply mode:

- Requires clean source and target repositories.
- Refuses a changed source commit, target commit, or plan digest.
- Copies only absent template-owned regular files.
- Creates target-specific process ownership and version metadata.
- Adds exact existing template-owned collisions to the target's project-owned protections.
- Rolls back files created during the run when an apply error occurs.
- Does not edit mixed files, project-owned docs, Git metadata, remotes, or external state.

If `.mamkin/process-manifest.json` or `.mamkin/template-version.json` already exists, treat the repository as initialized or partial. Do not overwrite either file; return the appropriate sync or recovery route.

## Project Reconciliation

After the deterministic seed, manually adapt only the approved surfaces:

- Merge Mamkin request routing, safety rules, and handoff boundaries into the existing `AGENTS.md`; preserve project architecture and coding rules.
- Keep `README.md` as the project entrypoint and add concise links instead of replacing established product documentation.
- Create `docs/project/brief.md`, `docs/project/decision-log.md`, and `features/00-roadmap.md` from repository evidence and interview decisions, not copied placeholders.
- Set one project prefix in `docs/process/naming-conventions.md`.
- Configure `.mamkin/validation-map.json` only with existing deterministic local argv commands. Do not create or install a formatter implicitly.
- Add project-local Codex runtime, MCP, hook, rule, or agent configuration only after the applicable human review.
- Create custom roles or skills only for an approved recurring need.

Keep product code, tests, migrations, deployment files, infrastructure, assets, secrets, and existing project-specific skills project-owned.

## Baseline Validation

Run relevant existing safe local checks against the adopted state. Prefer the repository's documented type, lint, unit, integration, end-to-end, build, and project-specific audit commands. Do not run secret-dependent, provider-mutating, production, destructive migration, installation, or networked checks without approval.

If checks are missing or fail, adoption may finish as `Adopted with baseline gaps` when the process layer and project sources are coherent. Record each failure, its proof boundary, and the first stabilization candidate. Never claim the upcoming product change caused a pre-existing baseline failure.

## Self-Review

Confirm:

- Existing files, product behavior, Git history, remotes, and deployment state were preserved.
- Source commit, target adoption commit, and ownership metadata are explicit.
- No secret value, private target, provider credential, or production data was captured.
- Mixed files preserve project-specific knowledge.
- Brief, decision log, roadmap, validation map, and human gates are usable or their exact gaps are reported.
- No upcoming product feature was implemented during adoption.
- The first coordinator action is one bounded, valuable, reversible slice or baseline-stabilization item.
- Project trust and hook review requirements are reported when project-local Codex surfaces were added.

## Handoff

Return `docs/process/handoff-packets/adoption.md`. Use `Adoption applied` only when the self-review passes and no required reconciliation remains. Use `Adopted with baseline gaps` when process adoption is complete but current checks or validation coverage have named gaps. Otherwise return the smallest blocker or review decision.

## Coordinator Transition

Completed adoption is a durable context boundary, not implicit authorization to start the first product slice in the same task.

1. Recommend a fresh, non-forked coordinator task using `docs/process/thread-operations.md` and the coordinator title in `docs/process/naming-conventions.md`.
2. Ask the human to choose: create the recommended fresh task, or explicitly continue here and approve renaming this task. Adoption approval and newly supplied feature requirements do not select either path.
3. After fresh-task approval, create the coordinator with the target repository as its project context and a standalone starter prompt grounded in the adoption handoff, brief, decision log, roadmap, and any newer human requirements. Verify receipt once, report its id, and stop product coordination in the adoption task.
4. If task tools are unavailable, return the exact starter prompt for manual paste.
5. Same-task continuation is allowed only when the human explicitly chooses it. Re-read the named current sources, rename the task to the coordinator pattern when approved and supported, then invoke `mamkin-coordinate` before feature work.

This is a post-adoption coordinator start, not a coordinator rollover: the adoption task never owned ongoing product coordination.

The adoption task owns the transition fields in the handoff. Initially record `fresh task recommended` and `waiting for human choice`. After fresh-task receipt, record the id/title, delivered prompt, and `adoption task complete - coordination transferred`; for same-task choice, record the explicit choice and approved rename before invoking `mamkin-coordinate`.
