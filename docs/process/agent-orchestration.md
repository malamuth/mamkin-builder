# Agent Orchestration

This is the coordinator manual. Workers should not read this whole file by default; give each worker the relevant role card, feature docs, and packet template instead.

## Customization Boundary

This file is durable process, not a live planning note. Put first-slice focus, current project recommendations, stack questions, and roadmap-specific guidance in `docs/project/brief.md`, `features/00-roadmap.md`, `docs/project/decision-log.md`, or the coordinator prompt.

Edit this file only when the coordination model, reusable workflow rules, custom-role wiring, or durable process-level human gates change.

## Reading Model

- Coordinator reads this file and the needed packet files.
- Workers read `AGENTS.md`, their role card under `docs/process/roles/`, the relevant feature or walkthrough docs, and only the packet file they must return.
- Read `docs/process/thread-operations.md` only when starting, receiving from, or recovering a separate worker lane.
- Long-lived implementation, review, walkthrough, deployment, and research lanes should run as separate Codex threads by default.
- Write-capable implementation and walkthrough/verification work must use separate Codex lanes/threads unless the human explicitly approves a same-thread subagent exception for that exact task.
- Same-thread subagents are only for bounded sidecar tasks, mock runs, quick read-only analysis, or experiments where the coordinator will immediately inspect and integrate the result.
- New worker/specialist lanes should be clean thread creations with standalone role prompts. Do not fork the coordinator thread to create implementation, walkthrough, review, deployment, or specialist lanes unless the human explicitly wants inherited conversation history.

## Source Authority

When facts conflict, use this authority order:

1. Current human decisions in the coordinator thread and durable decision records.
2. Current repo sources, manifests, project docs, feature specs, walkthroughs, and runbooks at the expected branch or commit.
3. Generated reports, logs, screenshots, external checks, or live proofs from a named branch/commit/environment.
4. Old handoff packets, old coordinator summaries, stale chat memory, and previous generated reports.

Old packets are useful history, not source of truth. If a packet conflicts with current human decisions or current files, explicitly treat that packet detail as obsolete and continue from the higher-authority source.

External proof has narrow scope. A live check, screenshot, generated report, preview, provider dashboard, API response, or other outside signal proves only the exact observed fact at the named state. It does not automatically prove architecture correctness, source ownership, merge readiness, or that generated artifacts match current source.

## Context Reset Triggers

Pause execution and perform a source-grounded reset when any of these happen:

- The coordinator repeats a fact the human or a source file already corrected.
- The thread starts treating old packets, summaries, or memory as authority over current files.
- The coordinator cannot name the source file, doc, report, branch, commit, or human decision behind an important claim.
- The thread over-focuses on a stale or low-importance detail while losing the main acceptance question.
- Generated artifacts, reports, or external checks disagree with source files or expected ownership.
- The human asks for a reset, detox, source check, or says the thread is hallucinating or drifting.

For small cases, the coordinator may do the reset inline by rereading the relevant current files and writing a short correction before continuing. For complex, multi-repo, integration, generated-artifact, data, deployment, or architecture-heavy work, route a read-only context reset to the architect lane or a custom specialist. Do not continue implementation, merge, deployment, or live validation until the reset identifies the current source of truth and obsolete assumptions.

## Architecture Restatement Gate

Before merge readiness, live/external validation, deployment handoff, or major routing in a complex lane, the coordinator must restate the current model or route that restatement to the architect. Include:

- The exact branch, commit, worktree, environment, or external target being reasoned about.
- The current source-of-truth docs/files/manifests and what each owns.
- The active scope, omitted scope, and any intentionally excluded concepts.
- The generated artifacts, reports, or external proofs being used, with their narrow meaning.
- Any old packet details or assumptions now considered obsolete.
- Remaining uncertainties and the lane that should resolve them.

This restatement should be short, but it must be source-grounded. If the coordinator cannot fill it without guessing, the next action is a blocker or architect/context reset lane, not implementation.

## Start Condition

Use this coordinator manual after the init agent has already adapted the copied template into a real project and handed off the project brief, decision log, and roadmap. If the project has not been initialized yet, run `docs/process/init-agent.md` first.

After init, the coordinator should call the architect before spinning implementation workers. Use an analyst first when the user/problem/domain/workflow is still fuzzy. The analyst clarifies what is being built and why; the architect clarifies how it should be structured and sliced.

When the user asks to create new features, the coordinator should usually call the architect first unless the change is already fully specified and low-risk.

## Default Feature Flow

```text
Coordinator -> Analyst if needed -> Architect -> Implementation worker -> optional reviewer -> walkthrough/testing -> Coordinator final report
```

Every non-coordinator agent returns its final packet to the coordinator. Agents should not hand work directly to peer agents or start follow-up threads unless the coordinator explicitly delegates that path.

## Thread Delivery Contract

Workers follow the handoff invariant in `AGENTS.md`. Every dynamic worker prompt supplies the exact coordinator thread id, return path, output packet, and stop rule. The coordinator confirms receipt before routing follow-up work.

For clean thread creation, start-health checks, manual-relay recovery, and polling boundaries, read `docs/process/thread-operations.md`.

## Decision Routing

Human decisions are coordinator-owned by default.

When a worker packet says `Needs human decision`, `Blocked` on a human gate, `Human judgment needed`, or `Human/manual steps expected`, the worker should return the packet to the coordinator and stop. The worker should not treat its own thread as the approval lane unless the coordinator prompt explicitly delegates that exact human question.

The coordinator then summarizes the options, asks the human in the coordinator thread, records durable decisions in `docs/project/decision-log.md` and the relevant brief/feature spec when needed, and resumes the lane with a new worker prompt or retest request.

If the coordinator delegates a human question to a specialist thread, the prompt must name the exact decision, allowed wording or scope, where to record the answer, and the packet expected afterward. Never delegate collection of secret values.

## Lane-Specific Clarifications

When a specialist lane is active or was recently used, route human follow-up questions about that lane back to the same specialist by default. The coordinator may acknowledge the question and forward it, but should not answer deployment, architecture, analysis, design, review, UX, or walkthrough clarifications inline unless the answer is purely administrative or the human explicitly asks the coordinator to decide.

When an implementation or inventory lane exists, route additional implementation, inventory, documentation-content, or artifact-update work to that lane by default. The coordinator may update coordination/process records inline, but should not keep changing feature artifacts or inventory content in the coordinator thread unless the human explicitly asks for a one-off inline edit and the coordinator records why it is safe.

Examples:

- Deployment/provider/setup/secrets questions -> deployment guide.
- Stack/API/data-model tradeoffs -> architect.
- User/problem/workflow ambiguity -> analyst.
- Verification/check results -> walkthrough/testing worker.
- Inventory/content corrections after implementation has started -> existing implementation worker or a new worker with explicit file ownership.

## After Human Decisions

When the coordinator receives human decisions for a specialist packet, it records the decisions and returns unresolved specialist work to that role by default.

Do not continue architecture, analysis, design, UX, deployment, review, or walkthrough work inside the coordinator thread unless the remaining work is trivial and the coordinator says why it is staying inline. For architecture and analysis especially, pass the human decision context back to the same specialist thread, or start a new specialist thread if the old one is unavailable.

Use the smallest useful team. After init, the first planning lane should usually include an architect and may include an analyst when product/domain understanding is fuzzy. For later narrow features, the team is often:

- coordinator
- one implementation worker
- one walkthrough/testing worker

For later feature work, add analyst, architect, designer, reviewer, UX reviewer, or deployment guide only when the feature has a clear need for that role.

## Role Cards

- Architect: `docs/process/roles/architect.md`; agent preset `mamkin-architect`.
- Analyst: `docs/process/roles/analyst.md`; agent preset `mamkin-analyst`.
- Implementation worker: `docs/process/roles/implementation.md`; agent preset `mamkin-worker`.
- Reviewer: `docs/process/roles/reviewer.md`; agent preset `mamkin-reviewer`.
- Walkthrough/test guide: `docs/process/roles/walkthrough.md`; agent preset `mamkin-walkthrough`.
- Deployment guide: `docs/process/roles/deployment.md`; agent preset `mamkin-deployment`.
- Designer: `docs/process/roles/designer.md`; agent preset `mamkin-designer`.
- UI/UX reviewer: `docs/process/roles/ux.md`; agent preset `mamkin-ux`.
- Custom recurring roles: add role cards under `docs/process/roles/` during init or coordinator-approved setup.

Packet templates are indexed in `docs/process/handoff-packets.md` and split under `docs/process/handoff-packets/`. Naming rules live in `docs/process/naming-conventions.md`.

## Agent Presets

Codex runtime presets live under `.codex/agents/`. They are short launch wrappers for sandbox, reasoning posture, and the handoff return path; they do not replace role cards, packet templates, or feature docs.

When starting a separate Codex thread for a built-in role, use the matching `mamkin-*` preset when the platform supports custom agents. If custom agents are unavailable, include the same role card, packet template, thread name, coordinator thread id, and return-path instructions directly in the prompt.

Preset sandbox, model, MCP, and reasoning settings are desired launch defaults. They do not replace human gates, file ownership rules, or the prompt's allowed-work boundary, because a running Codex session may apply live runtime approvals or inherited permissions when spawning a child. If a preset and the current runtime disagree, follow the stricter project process and ask the human before relying on broader access.

## Custom Roles

Use built-in roles unless the project needs a recurring specialist with distinct responsibilities. A custom role is ready to use only when it has a role card, a matching handoff packet, a custom agent preset when custom agents are supported, a thread naming rule, an invocation rule in the project brief or this file, and explicit human gates.

If a needed custom role is missing those artifacts, ask the human before scaffolding it or assigning an analyst/architect to define it. Do not invent a custom role only inside a worker prompt.

## Coordinator Duties

- Read project brief, decision log, roadmap, follow-ups, any relevant feature specs or walkthroughs, and current repo state.
- Apply the source authority order when facts conflict; do not let old packets, generated reports, external proof, or memory override current decisions and current files.
- Check `docs/follow-ups/` before planning; assess whether each unresolved follow-up should become part of the current feature, the next feature spec, a later roadmap candidate, or a deferred note.
- Before sending a next feature spec to an architect for fine-tuning, review all unimplemented follow-ups and explicitly decide which are relevant to that architect lane.
- Keep the roadmap status current at every feature-cycle transition: spec proposed/ready, implementation started, review or walkthrough started/completed, follow-ups deferred/resolved, and commit/push completed.
- Recommend the smallest useful team and ask the human before adding specialist roles.
- Use custom roles only after their role card, packet, custom agent preset when supported, naming rule, invocation rule, and human gates exist.
- Create or assign feature-spec drafting before implementation starts; init only creates roadmap candidates.
- Ensure every feature spec follows `docs/templates/feature-spec.md` unless the coordinator explicitly records why a different structure is needed.
- Define the implementation slice, pass/fail criteria, human gates, and handoff path.
- Own the walkthrough definition; write it or explicitly assign someone to draft/update it before walkthrough starts.
- Ensure every walkthrough follows `docs/templates/walkthrough.md` unless the coordinator explicitly records why a different structure is needed.
- Before starting implementation, prefer a clean planning baseline commit that contains the accepted feature spec, walkthrough/runbook, roadmap status, and relevant decisions. If committing is not approved or Git is unavailable, record the exact baseline state in the worker prompt instead.
- Start real team members as separate threads by default.
- Do not use same-turn subagents for write-capable implementation or walkthrough/verification lanes unless the human explicitly approved that exception. If thread creation is failing, return a manual starter prompt or ask the human how to proceed instead of silently changing execution mode for write-capable work.
- For parallel write-capable workers, use separate worktrees or explicitly disjoint `Allowed files to edit` ownership.
- Set the worker thread name from `docs/process/naming-conventions.md`, include it in the worker prompt, and rename or request rename if the platform auto-generates a different title.
- Follow `docs/process/thread-operations.md` for clean creation, start-health checks, delivery, receipt recovery, and fallback.
- Route lane-specific human clarifications to the active or most recent specialist instead of answering them inline.
- Route post-start implementation/inventory/content changes to the active or most recent implementation worker by default; the coordinator records decisions, packets, and routing, not the artifact changes themselves.
- Trigger a source-grounded context reset when the thread repeats corrected facts, loses source ownership, treats old packets as authority, or cannot cite the source behind important claims.
- Require an architecture restatement before complex merge, validation, deployment, or routing decisions when source ownership, generated artifacts, external proof, or multiple repos/components are involved.
- Delegate post-implementation verification lanes to walkthrough/testing workers, and delegate environment/provider setup lanes to deployment guides by default.
- Write focused worker prompts instead of making every worker read the whole orchestration manual.
- Pass the relevant feature spec, walkthrough, role card, and packet file explicitly in each worker prompt.
- Relay handoffs, defects, and retest requests without dropping technical details.
- Recommend `.codex/config.toml`, `.codex/rules/`, or process-doc corrections when repeated runtime or routing friction appears; ask before changing config/rules during feature work.
- Before final status, perform a coordinator quality gate: inspect returned packets, confirm expected files/scope, reconcile roadmap/docs/follow-ups, verify required checks were run or gaps are explicit, and look for obvious process or acceptance-rule violations. Route source or artifact fixes back to the proper lane instead of fixing them inline.
- Decide whether a result is merge-ready, verified with follow-ups, blocked, or not ready.
- After the final report, start, fork, or rename a fresh coordinator thread for the next coherent feature when context is heavy or the work direction changes.

## Worker Prompt Contract

Every worker prompt should include:

```text
Role:
Goal:
Success criteria:
Required evidence and source authority:
Scope and allowed files:
Human and permission boundaries:
Validation required:
Output packet:
Stop and fallback rules:
Project:
Feature/Slice:
Agent preset:
Thread name:
Worker thread id, if known:
Source thread:
Coordinator thread id:
Expected worktree:
Expected branch or commit:
Allowed worktree sharing: separate worktree | disjoint files only | read-only
Read first:
Do not edit:
Handoff return path:
```

The `Read first` list should stay short. Prefer:

- `AGENTS.md`
- one role card
- one feature spec or walkthrough, when one exists
- one relevant packet file
- any project docs necessary for the slice

Do not start implementation workers from roadmap candidates alone unless the coordinator writes an equivalent scoped brief directly in the prompt.

For `Thread name`, use `docs/process/naming-conventions.md`. If the platform creates a different title, rename the thread or request rename before treating the worker as properly started. Do not rely on auto-generated titles from the first prompt words.

Lead with the result the lane must produce. `Success criteria` names the observable completion bar; `Required evidence and source authority` names the inputs that support important claims; `Validation required` names checks that matter and how to report gaps.

For `Coordinator thread id`, provide the exact delivery target. `Worker thread id` is only an anti-self-send and recovery handle. `Handoff return path` supplies the direct-send target and the manual fallback required by `AGENTS.md`.

`Stop and fallback rules` should say `Return one packet, then stop`, and require a blocker packet when the worker cannot access required sources, reaches a human gate, or cannot satisfy the completion bar.

## Human Gates

Use these classifications in project docs, feature specs, and handoffs:

- `MUST involve human`: the agent must stop and ask.
- `SHOULD involve human`: the agent may recommend a default, but should surface the choice.
- `Agent may decide`: low-risk detail inside agreed scope.

Common `MUST involve human` gates:

- GitHub repo/project creation, external accounts, paid services, secrets, billing, DNS, production deployment, destructive migrations, private data import/export, public posting, legal/licensing decisions, system/global tooling installs, local database/service installs, Docker/Colima setup, Homebrew package installs, and scope changes that alter product promise or user privacy.

Common `SHOULD involve human` gates:

- Feature prioritization, naming, brand/visual direction, analytics, notification behavior, default retention, non-obvious UX tradeoffs, and architecture choices with long-term lock-in.

## Follow-Up Triage

Follow-ups should always be collected, but they are not automatically acceptance criteria for the active feature.

When a new follow-up arrives, the coordinator should classify it before routing work:

- Current feature: include only if it directly affects the feature's stated product value, acceptance criteria, or a defect in newly changed behavior.
- Current feature, optional follow-up: record it and implement only if it is small, low-risk, and does not destabilize the lane.
- Future feature: add or move it to the appropriate roadmap candidate or future feature spec.
- Deferred note: keep it in `docs/follow-ups/` when it is real but not yet scoped.

If a follow-up changes product direction, visual direction, public behavior, privacy, or integration scope, route it through the coordinator and update the feature spec or roadmap before sending it to workers.

Before creating or sending a feature doc to an architect, the coordinator must inspect unresolved follow-ups and tell the architect which ones are in scope, out of scope, or open for recommendation. Do not make the architect rediscover old follow-ups from scratch.

## Lifecycle

1. Kickoff: coordinator checks repo state, reads source docs, triages unresolved follow-ups, updates roadmap status if prior work moved, recommends team shape, and defines the planning lane.
2. Analysis pass: optional; use when user, problem, workflow, business rules, or domain constraints are unclear.
3. Architecture pass: use after init and whenever boundaries, data model, integrations, or tradeoffs are unclear; pass relevant unresolved follow-ups into the architect prompt and update the roadmap when a candidate becomes a ready feature spec.
4. Planning baseline: before implementation, prefer a clean commit containing the accepted feature spec, walkthrough/runbook, roadmap status, and relevant decisions. If a commit is not approved or Git is unavailable, record the exact baseline state in the worker prompt.
5. Implementation: worker implements one bounded slice and returns an implementation handoff; mark the feature in implementation when the lane starts.
6. Review: optional code/diff review before walkthrough; use when correctness, security, migration, API contract, or regression risk warrants a second engineering read; keep roadmap status aligned with review outcome.
7. Walkthrough: required acceptance verification after implementation or review; use to run the approved checks/manual flows against the exact branch/commit and decide merge readiness; record pass/blocker/follow-up status in the roadmap.
8. Coordinator quality gate: inspect packets, scope, docs, roadmap, checks, generated churn, and unresolved follow-ups before committing or reporting final status. Send fixes back to the correct lane.
9. Final report: coordinator records status, test gaps, human steps, follow-ups, commit/push state when applicable, and next action in both the final report and roadmap.

Use only the needed packet file from `docs/process/handoff-packets/` at each step.

Post-implementation verification is a separate lane. The coordinator should not run local/test database smoke, Docker smoke, deployment smoke, production setup, or provider setup inline by default. Use a walkthrough/testing worker for local and acceptance checks, and a deployment guide for environment, provider, or production setup. The coordinator may run a trivial already-available check inline only when it states why it is safe and no new tooling, service, account, secret, or production access is needed.

Walkthrough/testing workers should also run as separate Codex lanes by default. A same-thread subagent may summarize or inspect read-only evidence, but it should not be the acceptance walkthrough for a changed worktree unless the human explicitly approves that exception.

Approval of a verification lane does not approve installing missing tooling. If required local tooling is absent, stop and ask the human to choose: provide an existing endpoint/tool, approve a specific install/setup, use an already available alternative, or defer the check.

After init, the coordinator owns feature-spec and walkthrough creation. The coordinator may write them directly or assign drafting/update tasks, usually after an architect pass for the first project slice. The walkthrough worker normally executes the approved walkthrough; it should not invent acceptance criteria unless the coordinator explicitly asks for missing coverage to be drafted.

## Traceback Contract

Every meaningful feature should leave a clear path:

```text
Project brief -> decision log -> feature spec -> implementation handoff -> tests -> walkthrough -> follow-ups
```

Record durable decisions in `docs/project/decision-log.md`. Record non-blocking discovered work in `docs/follow-ups/`. Do not put temporary thread ownership, live branch status, or secrets in feature specs.

The roadmap should reflect the current durable feature state, not just initial spec creation. If roadmap status and feature docs disagree, update the roadmap before starting the next lane or finalizing a cycle.

## Context Health, Reset, And Rollover

Use `docs/process/context-health-audit.md` or `mamkin-context-audit` when source grounding or coordinator reliability is in doubt. The audit chooses normal continuation, watch, same-thread reset, or rollover.

A same-thread reset is read-only and uses `mamkin-context-reset`. An approved rollover uses `mamkin-coordinator-rollover` and `docs/process/handoff-packets/coordinator-reset.md`. The focused skills own their prerequisites, packet shape, thread operations, and stop rules; do not duplicate those protocols in ordinary coordinator context.

Rollover transfers coordinator authority and is not a Git-branching action. The outgoing coordinator stops feature coordination after transfer begins, and only one thread should remain visibly authoritative when cleanup tools are available.

## Git And GitHub

- Follow the Git, remote, external-write, and parallel-ownership gates in `AGENTS.md`.
- Verify repo state before each implementation or walkthrough and include the expected worktree and branch/commit in every worker prompt and final packet.
- Prefer a small accepted planning commit before implementation. If committing is unavailable or not approved, record the exact clean or dirty baseline in the worker prompt.
- Branches and worktrees isolate write-capable work; coordinator rollover alone does not need a new branch.
- If GitHub issues or projects are approved, keep them small enough to map to feature specs or bounded sub-slices.

## Completion Rules

- One implementation owner per slice; parallel writers need isolated or disjoint ownership.
- Test the exact expected branch/commit and keep external proof narrower than the claim it supports.
- Route source confusion to context audit/reset instead of continuing from memory.
- Keep coordinator, implementation, review, walkthrough, and deployment ownership distinct once their lanes exist.
- Final status must name validation run, validation omitted, remaining human steps, follow-ups, and the next action.
