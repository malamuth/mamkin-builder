# Agent Orchestration

This is the coordinator/team-lead manual. Workers should not read this whole file by default; give each worker the relevant role card, feature docs, and packet template instead.

## Customization Boundary

This file is durable process, not a live planning note. Put first-slice focus, current project recommendations, stack questions, and roadmap-specific guidance in `docs/project/brief.md`, `features/00-roadmap.md`, `docs/project/decision-log.md`, or the coordinator prompt.

Edit this file only when the coordination model, reusable workflow rules, custom-role wiring, or durable process-level human gates change.

## Reading Model

- Coordinator/team lead reads this file and the needed packet files.
- Workers read `AGENTS.md`, their role card under `docs/process/roles/`, the relevant feature or walkthrough docs, and only the packet file they must return.
- Long-lived implementation, review, walkthrough, deployment, and research team members should usually run as separate Codex threads.
- Same-thread subagents are for bounded sidecar tasks, mock runs, quick analysis, or experiments where the coordinator will immediately inspect and integrate the result.

## Start Condition

Use this coordinator manual after the init agent has already adapted the copied template into a real project and handed off the project brief, decision log, and roadmap. If the project has not been initialized yet, run `docs/process/init-agent.md` first.

After init, the coordinator should call the architect before spinning implementation workers. Use an analyst first when the user/problem/domain/workflow is still fuzzy. The analyst clarifies what is being built and why; the architect clarifies how it should be structured and sliced.

When the user asks to create new features, the coordinator should usually call the architect first unless the change is already fully specified and low-risk.

## Default Feature Flow

```text
Coordinator/team lead -> Analyst if needed -> Architect -> Implementation worker -> Review/walkthrough -> Coordinator final report
```

Every non-coordinator agent returns its final packet to the coordinator. Agents should not hand work directly to peer agents or start follow-up threads unless the coordinator explicitly delegates that path.

## Thread Delivery Contract

Separate worker threads do not imply automatic cross-thread delivery.

Every worker prompt must specify the physical return path. If thread tools are available and explicitly delegated, the worker may send the final packet to the coordinator thread. Otherwise, the worker returns a coordinator-ready packet in its own thread and labels it `Coordinator handoff`.

The coordinator is responsible for collecting, reading, or pasting worker packets before continuing the lane.

## Decision Routing

Human decisions are coordinator-owned by default.

When a worker packet says `Needs human decision`, `Blocked` on a human gate, `Human judgment needed`, or `Human/manual steps expected`, the worker should return the packet to the coordinator and stop. The worker should not treat its own thread as the approval lane unless the coordinator prompt explicitly delegates that exact human question.

The coordinator then summarizes the options, asks the human in the coordinator thread, records durable decisions in `docs/project/decision-log.md` and the relevant brief/feature spec when needed, and resumes the lane with a new worker prompt or retest request.

If the coordinator delegates a human question to a specialist thread, the prompt must name the exact decision, allowed wording or scope, where to record the answer, and the packet expected afterward. Never delegate collection of secret values.

## After Human Decisions

When the coordinator receives human decisions for a specialist packet, it records the decisions and returns unresolved specialist work to that role by default.

Do not continue architecture, analysis, UX, deployment, review, or walkthrough work inside the coordinator thread unless the remaining work is trivial and the coordinator says why it is staying inline. For architecture and analysis especially, pass the human decision context back to the same specialist thread, or start a new specialist thread if the old one is unavailable.

Use the smallest useful team. After init, the first planning lane should usually include an architect and may include an analyst when product/domain understanding is fuzzy. For later narrow features, the team is often:

- coordinator/team lead
- one implementation worker
- one walkthrough/testing worker

For later feature work, add analyst, architect, reviewer, UX reviewer, or deployment guide only when the feature has a clear need for that role.

## Role Cards

- Architect: `docs/process/roles/architect.md`
- Analyst: `docs/process/roles/analyst.md`
- Implementation worker: `docs/process/roles/implementation.md`
- Reviewer: `docs/process/roles/reviewer.md`
- Walkthrough/test guide: `docs/process/roles/walkthrough.md`
- Deployment guide: `docs/process/roles/deployment.md`
- UI/UX reviewer: `docs/process/roles/ux.md`
- Custom recurring roles: add role cards under `docs/process/roles/` during init or coordinator-approved setup.

Packet templates are indexed in `docs/process/handoff-packets.md` and split under `docs/process/handoff-packets/`. Naming rules live in `docs/process/naming-conventions.md`.

## Custom Roles

Use built-in roles unless the project needs a recurring specialist with distinct responsibilities. A custom role is ready to use only when it has a role card, a matching handoff packet, a thread naming rule, an invocation rule in the project brief or this file, and explicit human gates.

If a needed custom role is missing those artifacts, ask the human before scaffolding it or assigning an analyst/architect to define it. Do not invent a custom role only inside a worker prompt.

## Coordinator Duties

- Read project brief, decision log, roadmap, follow-ups, any relevant feature specs or walkthroughs, and current repo state.
- Check `docs/follow-ups/` before planning; assess whether any follow-up should become part of the next feature spec or roadmap update.
- Recommend the smallest useful team and ask the human before adding specialist roles.
- Use custom roles only after their role card and packet exist.
- Create or assign feature-spec drafting before implementation starts; init only creates roadmap candidates.
- Ensure every feature spec follows `docs/templates/feature-spec.md` unless the coordinator explicitly records why a different structure is needed.
- Define the implementation slice, pass/fail criteria, human gates, and handoff path.
- Own the walkthrough definition; write it or explicitly assign someone to draft/update it before walkthrough starts.
- Ensure every walkthrough follows `docs/templates/walkthrough.md` unless the coordinator explicitly records why a different structure is needed.
- Start real team members as separate threads by default.
- Write focused worker prompts instead of making every worker read the whole orchestration manual.
- Pass the relevant feature spec, walkthrough, role card, and packet file explicitly in each worker prompt.
- Relay handoffs, defects, and retest requests without dropping technical details.
- Decide whether a result is merge-ready, verified with follow-ups, blocked, or not ready.

## Worker Prompt Contract

Every worker prompt should include:

```text
Project:
Role:
Feature/Slice:
Source thread:
Expected worktree:
Expected branch or commit:
Read first:
Allowed files to edit:
Do not edit:
Handoff target: coordinator
Physical return path:
Human decision routing:
Stop condition:
Expected final packet:
```

The `Read first` list should stay short. Prefer:

- `AGENTS.md`
- one role card
- one feature spec or walkthrough, when one exists
- one relevant packet file
- any project docs necessary for the slice

Do not start implementation workers from roadmap candidates alone unless the coordinator writes an equivalent scoped brief directly in the prompt.

For `Human decision routing`, default to `Return human gates to coordinator; do not ask the human directly in this thread`.

For `Physical return path`, default to `Return a coordinator-ready packet in this thread labeled Coordinator handoff; do not assume automatic cross-thread delivery`.

## Human Gates

Use these classifications in project docs, feature specs, and handoffs:

- `MUST involve human`: the agent must stop and ask.
- `SHOULD involve human`: the agent may recommend a default, but should surface the choice.
- `Agent may decide`: low-risk detail inside agreed scope.

Common `MUST involve human` gates:

- GitHub repo/project creation, external accounts, paid services, secrets, billing, DNS, production deployment, destructive migrations, private data import/export, public posting, legal/licensing decisions, and scope changes that alter product promise or user privacy.

Common `SHOULD involve human` gates:

- Feature prioritization, naming, brand/visual direction, analytics, notification behavior, default retention, non-obvious UX tradeoffs, and architecture choices with long-term lock-in.

## Lifecycle

1. Kickoff: coordinator checks repo state, reads source docs, recommends team shape, and defines the planning lane.
2. Analysis pass: optional; use when user, problem, workflow, business rules, or domain constraints are unclear.
3. Architecture pass: use after init and whenever boundaries, data model, integrations, or tradeoffs are unclear.
4. Implementation: worker implements one bounded slice and returns an implementation handoff.
5. Review: optional code/diff review before walkthrough; use when correctness, security, migration, API contract, or regression risk warrants a second engineering read.
6. Walkthrough: acceptance verification after implementation or review; use to run the approved checks/manual flows against the exact branch/commit and decide merge readiness.
7. Final report: coordinator records status, test gaps, human steps, follow-ups, and next action.

Use only the needed packet file from `docs/process/handoff-packets/` at each step.

After init, the coordinator owns feature-spec and walkthrough creation. The coordinator may write them directly or assign drafting/update tasks, usually after an architect pass for the first project slice. The walkthrough worker normally executes the approved walkthrough; it should not invent acceptance criteria unless the coordinator explicitly asks for missing coverage to be drafted.

## Traceback Contract

Every meaningful feature should leave a clear path:

```text
Project brief -> decision log -> feature spec -> implementation handoff -> tests -> walkthrough -> follow-ups
```

Record durable decisions in `docs/project/decision-log.md`. Record non-blocking discovered work in `docs/follow-ups/`. Do not put temporary thread ownership, live branch status, or secrets in feature specs.

## Git And GitHub

- Verify repo state before each implementation or walkthrough.
- If git is not initialized, ask before `git init`.
- If no initial commit exists, propose one after docs are adapted.
- Ask before creating remotes, pushing, creating GitHub issues, milestones, or project boards.
- If GitHub Projects are used, keep issues small enough to map to feature specs or sub-slices.
- Mention expected branch/commit in every worker prompt and final packet.

## Failure Prevention

- Do not run duplicate implementation workers for the same slice.
- Do not test the wrong branch or worktree.
- Do not let workers silently expand scope.
- Do not edit active feature specs during implementation unless explicitly assigned.
- Do not hide test gaps behind a confident final sentence.
- Do not paste secrets into docs or chat.
- Do not create production resources without human approval.
