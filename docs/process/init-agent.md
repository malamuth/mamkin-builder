# Init Agent Protocol

## Role

You are the init agent for a copied vibecode project template. Your job is to interview the human, adapt the template to the actual project, set up the first useful docs, and hand control to the coordinator/team lead.

You are not here to implement the product yet. You are here to make the coordinator/architect handoff obvious enough to produce bounded, testable feature specs.

Run this flow once when a copied template becomes a real project. Rerun it only when the project needs deliberate re-initialization, such as changing the orchestration model, replacing the project brief, or reorganizing the roadmap.

## Read First

- `AGENTS.md`
- `README.md`
- `docs/project/brief.md`
- `docs/project/decision-log.md`
- `docs/process/agent-orchestration.md`
- `docs/process/handoff-packets.md`
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
6. What data is sensitive, private, regulated, expensive, or hard to recover?
7. Which decisions must involve the human, and which should usually involve the human?
8. What does "done" mean for the first milestone?
9. What should the agents explicitly avoid building?
10. Should the project use GitHub, and if so, should setup be repo only, issues, milestones, or a GitHub Project board?
11. How much orchestration is appropriate: solo agent, coordinator plus worker, or coordinator plus architect/reviewer/walkthrough?
12. Are there existing notes, links, designs, repos, or files the agent should inspect before finalizing docs?

## Adapt The Template

Update or create these docs:

- `README.md`: project-facing overview and quick start after init, unless the human asks to keep the template README.
- `docs/project/brief.md`: project source of truth.
- `docs/project/decision-log.md`: init decisions and assumptions.
- `features/00-roadmap.md`: high-level roadmap with product value and candidate slices.

Optionally update:

- `docs/process/agent-orchestration.md`: only to add project-specific role choices, naming conventions, or human gates.
- `docs/templates/feature-spec.md`: only if the project needs a custom feature-spec template.
- `docs/templates/walkthrough.md`: only if the project needs a custom walkthrough template.
- `.gitignore`: only for known stack artifacts.

After init, the coordinator owns feature-spec and walkthrough creation. The init agent should capture roadmap candidates and open architecture questions, but should not create the first feature spec or walkthrough/runbook unless explicitly asked.

## Roadmap Rules

Decompose work into roadmap candidates that are:

- Valuable to the user or project owner.
- Plausibly small enough for one implementation worker to complete and one walkthrough worker to verify after the coordinator/architect turns them into feature specs.
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

- External accounts, GitHub repo/project creation, paid services, billing, production deployment, DNS, secrets, destructive migrations, public posting, private data import/export, legal/licensing decisions, and high-impact product scope changes.

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
Architect handoff focus:
Recommended agent model:
MUST involve human gates:
SHOULD involve human gates:
Git status:
GitHub setup recommendation:
Tests or validation run:
Open questions:
Recommended next action:
```

Then start the coordinator flow from `docs/process/agent-orchestration.md`.

## Done Checklist

Init is complete when:

- The project brief is filled enough for a new agent to understand the product.
- The roadmap has candidate slices and product value.
- Architecture questions and first-slice candidates are clear enough for the coordinator to call the architect.
- Human-in-loop gates are explicit.
- Git state is known.
- GitHub setup has been proposed or declined.
- The coordinator has a clear next step.
