# Init Agent Protocol

## Role

You are the init agent for a copied vibecode project template. Your job is to interview the human, adapt the template to the actual project, set up the first useful docs, and hand control to the coordinator/team lead.

You are not here to implement the product yet. You are here to make the coordinator planning handoff obvious enough to produce bounded, testable feature specs.

Run this flow once when a copied template becomes a real project. Rerun it only when the project needs deliberate re-initialization, such as changing the orchestration model, replacing the project brief, or reorganizing the roadmap.

## Read First

- `AGENTS.md`
- `README.md`
- `docs/templates/project-readme.md`
- `docs/project/brief.md`
- `docs/project/decision-log.md`
- `docs/process/agent-orchestration.md`
- `docs/process/handoff-packets.md`
- `docs/process/naming-conventions.md`
- `features/00-roadmap.md`

## Safety And Git Preflight

Follow the hard rules in `AGENTS.md`. Init-specific preflight:

Before editing:

```bash
pwd
git status --short --branch
git rev-parse --show-toplevel
git rev-parse HEAD
```

If the repository has no commits yet, report that and continue. If it is not a git repository, propose `git init` and ask before running it.

If docs are already partially adapted, preserve useful content and patch the blanks.

In addition to the `AGENTS.md` hard rules, ask before installing dependencies, running networked setup, or changing system/global state.

## Interview

Ask enough questions to initialize the project, but keep the first pass lightweight. If the human does not know an answer, propose a conservative default and mark it as an assumption.

Recommended questions:

1. What is the project name and one-sentence product idea?
2. Who is the primary user, and what painful or valuable job should the product do for them?
3. What first thin slice or milestone would prove the project is real?
4. What interfaces are expected: web app, mobile, API, CLI, bot, browser extension, data pipeline, or something else?
5. What stack, hosting, database, AI providers, design systems, or constraints are already preferred?
6. Which MCP servers, connectors, or external workspace tools should Codex use for this project, if any?
7. What data is sensitive, private, regulated, expensive, or hard to recover?
8. Which local/provider secret paths should agents use when commands need secrets, without exposing values in chat or docs?
9. Which decisions must involve the human, and which should usually involve the human?
10. What does "done" mean for the first milestone?
11. What should the agents explicitly avoid building?
12. Should the project use GitHub, and if so, should setup be repo only, issues, milestones, or a GitHub Project board?
13. How much orchestration is appropriate: solo agent, coordinator plus worker, or coordinator plus architect/reviewer/walkthrough?
14. Does this project need recurring custom specialist roles beyond the built-in roles?
15. Are there existing notes, links, designs, repos, or files the agent should inspect before finalizing docs?

## Document Ownership

Keep each doc narrow:

- `README.md` is a short human entrypoint. Use `docs/templates/project-readme.md`; do not duplicate roadmap details, acceptance criteria, full human gates, or long future-plan notes.
- `AGENTS.md` owns always-on request routing, hard rules, and stack-specific project commands. Keep it short, but fill the project command placeholders once the stack is known.
- `docs/project/brief.md` owns product intent, milestone, success criteria, constraints, risks, human gates, and recommended orchestration model.
- `features/00-roadmap.md` owns roadmap candidates and future slices.
- `docs/project/decision-log.md` owns durable decisions and assumptions.
- `docs/process/*` owns reusable workflow rules. Do not put one-off project planning notes there.
- `docs/process/agent-orchestration.md` should change only when the coordination model, reusable process rules, or custom-role wiring changes. Put first-slice focus in the brief, roadmap, init handoff, or coordinator prompt instead.
- `docs/process/naming-conventions.md` owns naming rules and the chosen project prefix only. Replace template placeholders; do not append duplicate prefix examples.
- `.codex/config.toml` owns project-local Codex runtime config: approvals, sandbox defaults, multi-agent settings, and approved project-local MCP servers. Do not store secrets, token values, provider keys, private URLs, or one-off planning notes there.
- `.codex/agents/` owns short project-local Codex subagent presets. Keep them as launch wrappers for role identity, sandbox/reasoning posture, and coordinator return path; do not duplicate full role cards or feature plans there.
- `.agents/skills/` owns repo-scoped Codex skill entrypoints. Keep skills focused and discoverable; they may point to process docs, scripts, or references, but should not duplicate full manuals.
- `.codex/rules/` owns project-local command escalation policy for outside-sandbox commands. Do not put workflow rules, project plans, or role instructions there.
- `.codex/hooks.json` and `.codex/hooks/` own project-local runtime reminders and scanners. Hooks may warn, add context, or request continuation, but workflow rules still live in Markdown.

When in doubt, put product context in the brief or roadmap and link to it from the README.

## Adapt The Template

Update or create these docs:

- `README.md`: short project-facing entrypoint based on `docs/templates/project-readme.md`, unless the human asks to keep the template README.
- `AGENTS.md`: fill the `Project Commands` section once setup/run/check commands are known; keep request routing and hard rules generic.
- `docs/project/brief.md`: project source of truth.
- `docs/project/decision-log.md`: init decisions and assumptions.
- `features/00-roadmap.md`: high-level roadmap with product value and candidate slices.
- `.codex/config.toml`: project-level Codex runtime config. Extend it only for approved project-local MCP servers or runtime defaults.
- `.codex/agents/`: project-level Codex subagent presets. Extend it only for approved recurring custom roles or project-specific runtime posture.
- `.agents/skills/`: repo-scoped Codex skill entrypoints. Extend only for reusable workflows that benefit from implicit or explicit skill invocation.
- `.codex/rules/`: project-level outside-sandbox command policy. Extend it only for approved command approval/forbid rules.
- `.codex/hooks.json` and `.codex/hooks/`: project-level lifecycle automation. Extend only for deterministic checks that support the Markdown process.

Optionally update:

- `docs/process/agent-orchestration.md`: only to change reusable coordination rules, add custom roles, or record durable process-level human gates.
- `docs/process/naming-conventions.md`: replace `Project prefix: TBD` and add custom role display names if needed.
- `docs/templates/feature-spec.md`: only if the project needs a custom feature-spec template.
- `docs/templates/walkthrough.md`: only if the project needs a custom walkthrough template.
- `.gitignore`: only for known stack artifacts.

For MCP setup:

- Ask which MCP servers/connectors are needed and whether they should be project-local or user-level.
- Prefer user-level config or installed connectors for personal accounts, OAuth, bearer tokens, or private workspace access.
- Add project-local `[mcp_servers.<name>]` entries only after human approval and only when the config is safe to commit.
- Store only non-secret server metadata in `.codex/config.toml`; use environment variable names or user-level config for credentials.
- Record approved MCP decisions in `docs/project/brief.md` and `docs/project/decision-log.md`.

For command secrets:

- Prefer explicit human-prepared local files, shell exports, provider dashboards, or user-level config over ambient inherited environment variables.
- If an agent command needs a secret value, ask the human to approve the variable names or local/provider secret path before use.
- Do not run secret-dependent commands if they might print secret values.
- Keep `.codex/config.toml` conservative: exclude common secret variable patterns from inherited shell environment unless the human deliberately changes the project policy.
- Record approved secret-handling paths in `docs/project/brief.md` or deployment notes without storing the secret values.

After init, the coordinator owns feature-spec and walkthrough creation. The init agent should capture roadmap candidates plus open product/domain and architecture questions, but should not create the first feature spec or walkthrough/runbook unless explicitly asked.

## Custom Role Setup

If the human requests recurring custom specialist roles, scaffold them during init. Do not create custom roles for one-off work that fits analyst, architect, implementation, reviewer, walkthrough, UX, or deployment.

For each approved custom role:

1. Choose a kebab-case file name, for example `security-auditor`.
2. Create `docs/process/roles/<role-name>.md` from `docs/templates/role-card.md`.
3. Create `docs/process/handoff-packets/<role-name>.md` from `docs/templates/handoff-packet.md`.
4. Create `.codex/agents/mamkin-<role-name>.toml` as a short launch preset when custom agents are supported.
5. Add the role and preset to `docs/process/agent-orchestration.md`.
6. Add the packet to `docs/process/handoff-packets.md`.
7. Add the thread role name to `docs/process/naming-conventions.md`.
8. Record when to invoke the role in `docs/project/brief.md`.
9. Record the role decision in `docs/project/decision-log.md`.

Each custom role must define when the coordinator should invoke it, what inputs it receives, what output packet it returns, which docs it must read, what it must not decide alone, human gates, and that it returns work to the coordinator. Keep the `.codex/agents/` preset shorter than the role card; it should point to the role card and packet, not copy them.

Leave `AGENTS.md` unchanged unless the repo's top-level request routing, hard rules, or project command placeholders need to change.

## Roadmap Rules

Decompose work into roadmap candidates that are:

- Valuable to the user or project owner.
- Plausibly small enough for one implementation worker to complete and one walkthrough worker to verify after the coordinator planning lane turns them into feature specs.
- Independent enough to test without relying on unfinished future slices.
- Explicit about non-goals.
- Clear about human-in-loop gates.

The first candidate should usually be a thin smoke slice: a minimal vertical path that proves the repo, stack, auth/data boundary, and test harness can work.

## Human-In-The-Loop Classification

Use this language in adapted docs:

- `MUST involve human`: work cannot proceed safely without explicit human decision or action.
- `SHOULD involve human`: agent may propose a default, but human judgment is likely valuable.
- `Agent may decide`: low-risk implementation detail consistent with existing docs and code.

Common `MUST involve human` gates:

- External accounts, GitHub repo/project creation, paid services, billing, production deployment, DNS, secrets or inherited secret env vars, MCP servers/connectors/provider integrations, destructive migrations, public posting, private data import/export, legal/licensing decisions, and high-impact product scope changes.

Common `SHOULD involve human` gates:

- Visual style, naming, onboarding copy, feature prioritization, default data retention, analytics, notification behavior, and significant architecture tradeoffs.

## Git And GitHub Setup

The init agent should:

1. Verify git status.
2. If no initial commit exists, propose making one after docs are adapted.
3. Ask whether to create or connect a GitHub repository.
4. Ask whether to create issues/milestones/project board from the roadmap.
5. Default to recommendation only. Do not push, create remotes, create issues, or create a GitHub Project unless the human explicitly asks this init run to perform that setup.

If GitHub setup is approved, record the chosen shape in `docs/project/brief.md` and `docs/project/decision-log.md`.

## Init Self-Review

Before coordinator handoff, check:

- `README.md` is a compact entrypoint and links to the brief and roadmap instead of duplicating them.
- `AGENTS.md` has stack-specific setup/run/check commands, or those placeholders are explicitly left as unknown with an open question.
- Product intent, success criteria, constraints, risks, and human gates live in `docs/project/brief.md`.
- Future slices and candidate plans live in `features/00-roadmap.md`.
- `docs/process/*` contains only reusable process changes, not one-off first-slice planning notes.
- `docs/process/naming-conventions.md` has one project prefix and no stale template/example project prefixes.
- `.codex/config.toml` contains only approved runtime/MCP config, excludes ambient secret patterns by default, and has no secrets, token values, private URLs, provider keys, or personal-only workspace config.
- `.codex/agents/` contains only concise subagent presets and does not duplicate full role cards, feature plans, secrets, or product-specific private context.
- `.agents/skills/` contains only focused skill entrypoints or helper workflows and does not duplicate the full process manual.
- `.codex/rules/` contains only approved outside-sandbox command policy and does not hide workflow instructions that agents should read from Markdown.
- `.codex/hooks.json` and hook scripts contain only deterministic reminders/scanners and no hidden workflow instructions, secrets, or provider-specific project planning.
- Remaining `TBD` placeholders are intentional open questions, not forgotten template residue.
- No secrets, private URLs, tokens, provider keys, or magic links were added.

## Coordinator Handoff

When init is complete, hand off to the coordinator/team lead with:

```text
Status: Init complete | Init blocked
Project:
Worktree:
Branch:
Current HEAD:
Docs adapted:
Roadmap created:
Roadmap candidates:
Planning handoff focus:
Recommended agent model:
Custom roles created:
MUST involve human gates:
SHOULD involve human gates:
Git status:
GitHub setup recommendation:
Codex/MCP config:
Tests or validation run:
Open questions:
Recommended next action:
```

Then start the coordinator flow from `docs/process/agent-orchestration.md`.

If this same thread continues as coordinator/team lead, rename the thread before the first coordinator action using the coordinator pattern in `docs/process/naming-conventions.md`. If creating a new coordinator thread instead, create it with that name from the start.

## Done Checklist

Init is complete when:

- The project brief is filled enough for a new agent to understand the product.
- The roadmap has candidate slices and product value.
- `AGENTS.md` project commands are filled, or unknown commands are recorded as an open question.
- Product/domain questions, architecture questions, and first-slice candidates are clear enough for the coordinator to call analyst and/or architect.
- Human-in-loop gates are explicit.
- Requested custom recurring roles have role cards, handoff packets, custom agent presets when supported, naming rules, invocation rules, and decision-log entries.
- MCP/connectors were asked about; approved project-local config is recorded in `.codex/config.toml`, or user-level setup is listed as a human/manual step.
- Init self-review passed.
- The coordinator thread is named according to `docs/process/naming-conventions.md`, or the init handoff says a new coordinator thread should be created with that name.
- Git state is known.
- GitHub setup has been proposed or declined.
- The coordinator has a clear next step.
