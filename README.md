# Universal Vibecode Project Template

A tiny, product-agnostic starting point for vibecode projects. Copy it, ask an init agent to run the setup flow, and the agent will interview you, adapt the docs to the specific product, propose git/GitHub setup, and hand off to a coordinator-led implementation workflow.

The workflow is built for projects run by an init agent, a coordinator, optional analyst/architect/designer support, implementation workers, and walkthrough/testing agents. `AGENTS.md` stays short as the agent entrypoint; the durable process lives in `docs/process/`.

## Quick Start

1. Copy this repository for a new project. If you duplicate the folder directly, the hidden `.git/` directory is copied too, including branch, dirty state, and remotes. Treat that Git state as inherited template state until init decides what to keep.
2. Ask your agent to run the repo skill if available:

   ```text
   $mamkin-init
   ```

   Or use the plain prompt:

   ```text
   Read AGENTS.md and run the project init flow.
   ```

3. Answer the init questions.
4. Let the init agent adapt:
   - `README.md` from `docs/templates/project-readme.md`
   - `docs/project/brief.md`
   - `docs/project/decision-log.md`
   - `features/00-roadmap.md`
   - `AGENTS.md` project commands once the stack is known
   - the project prefix in `docs/process/naming-conventions.md`
   - `.mamkin/template-version.json` with the copied template baseline when known
   - approved project-local Codex config, hooks, rules, skills, or agent presets
   - process docs only when the reusable workflow or custom roles change
   - custom role cards and packets, if the project needs recurring specialist roles
5. The init agent verifies git state, calls out any inherited template branch, dirty state, or remote, proposes GitHub setup, and hands off to the coordinator flow.

## Start From GitHub

If you want the fresh published template but a new project that is not the `mamkin-builder` repo, first create and enter your new project folder. Then clone the template into that folder and detach the copied Git history before init:

```bash
mkdir my-new-project
cd my-new-project
git clone https://github.com/malamuth/mamkin-builder.git .
rm -rf .git
```

Then open this same folder in Codex and run:

```text
$mamkin-init
```

During init, decide whether to keep the project without Git for now, run `git init`, or connect a project-specific remote. Local `git init`, staging, and committing may still ask for approval because they write Git metadata. Do not push project commits back to `https://github.com/malamuth/mamkin-builder.git`.

## Why This Shape

Use `AGENTS.md` as the entrypoint because many coding agents already look for it. Keep it concise so every worker sees only high-signal rules. Put the coordinator manual, role cards, handoff packets, and testing contracts under `docs/process/`.

Use `.mamkin/` metadata to keep copied projects aligned with future template improvements. `mamkin-template-sync` updates the reusable process layer from the upstream template while protecting project-owned docs, feature specs, code, secrets, and remotes.

## Included Files

- `AGENTS.md`: short always-on agent entrypoint.
- `.agents/skills/`: repo-scoped Codex skill entrypoints.
- `.mamkin/`: template version and file ownership metadata for safe process sync.
- `.codex/agents/`: project-scoped Codex custom agent presets.
- `.codex/config.toml`: conservative project Codex runtime defaults.
- `.codex/hooks.json` and `.codex/hooks/`: project lifecycle reminders and scanners.
- `.codex/rules/`: project-local outside-sandbox command policy.
- `docs/process/init-agent.md`: project initialization protocol and questionnaire.
- `docs/process/agent-orchestration.md`: coordinator orchestration manual.
- `docs/process/context-health-audit.md`: read-only audit protocol for OK/watch/context reset/rollover decisions.
- `docs/process/template-sync.md`: safe sync protocol for updating copied projects from the current template.
- `docs/process/naming-conventions.md`: doc and agent-thread naming rules.
- `docs/process/roles/*.md`: small role cards for non-coordinator worker threads.
- `docs/process/handoff-packets.md`: index of shared packet templates.
- `docs/process/handoff-packets/*.md`: individual kickoff, handoff, defect, retest, and final report templates.
- `docs/project/brief.md`: adapted project source of truth.
- `docs/project/decision-log.md`: durable trace of important decisions.
- `docs/walkthroughs/`: coordinator-owned walkthroughs for implemented slices.
- `docs/follow-ups/`: completed test notes and non-blocking follow-up work.
- `features/README.md`: feature-spec folder guide.
- `features/00-roadmap.md`: roadmap candidates created or refined during init.
- `docs/templates/project-readme.md`: compact README shape for initialized projects.
- `docs/templates/feature-spec.md`: feature spec template.
- `docs/templates/walkthrough.md`: coordinator-owned walkthrough/runbook template.
- `docs/templates/role-card.md`: scaffold for custom recurring specialist roles.
- `docs/templates/handoff-packet.md`: scaffold for custom role handoff packets.

## Design Principles

- Keep `AGENTS.md` short and use it as a pointer to durable process docs.
- Put known setup/run/check commands in `AGENTS.md` so agents can verify work without guessing.
- Keep `README.md` lightweight; the brief and roadmap own product detail.
- Keep live coordination state out of feature specs.
- Require every feature to include product value, acceptance criteria, test plan, manual walkthrough, and human-in-loop gates.
- Use a coordinator-led flow rather than loose worker-to-worker relay.
- Make traceback explicit: project brief -> feature spec -> implementation handoff -> tests -> walkthrough -> follow-ups.
- Treat GitHub/project setup, production actions, secrets, and ambiguous product calls as human approval gates.
- Treat copied-project Git state and remotes as `TBD` until the human approves a project-specific repo; never push project commits to the template repo.

## Normal Operating Loop

1. Init agent interviews the human and adapts docs.
2. Coordinator reviews the project brief and roadmap.
3. Coordinator calls analyst if the domain is fuzzy, then architect to polish architecture and feature boundaries.
4. Coordinator creates or assigns one bounded feature spec and walkthrough definition.
5. Worker implements and returns a handoff packet.
6. Optional reviewer inspects the completed diff when risk warrants it.
7. Walkthrough/testing agent verifies the exact branch/commit.
8. Coordinator records results, follow-ups, and the recommended next action.

The goal is a predictable process with enough structure to stay clean, but not so much ceremony that a small project becomes a bureaucracy cosplay.
