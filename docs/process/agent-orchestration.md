# Agent Orchestration

This is the coordinator manual. Workers should not read this whole file by default; give each worker the relevant role card, feature docs, and packet template instead.

## Customization Boundary

This file is durable process, not a live planning note. Put first-slice focus, current project recommendations, stack questions, and roadmap-specific guidance in `docs/project/brief.md`, `features/00-roadmap.md`, `docs/project/decision-log.md`, or the coordinator prompt.

Edit this file only when the coordination model, reusable workflow rules, custom-role wiring, or durable process-level human gates change.

## Reading Model

- Coordinator reads this file and the needed packet files.
- Workers read `AGENTS.md`, their role card under `docs/process/roles/`, the relevant feature or walkthrough docs, and only the packet file they must return.
- Long-lived implementation, review, walkthrough, deployment, and research lanes should run as separate Codex threads by default.
- Same-thread subagents are only for bounded sidecar tasks, mock runs, quick analysis, or experiments where the coordinator will immediately inspect and integrate the result.

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

Separate worker threads can return packets directly when thread tools and the coordinator thread id are available, but cross-thread delivery is not guaranteed.

Every worker prompt must specify the coordinator thread id and handoff return path. Preferred path: when the prompt provides an exact coordinator thread id and a thread-send tool is available, send the final packet directly to that coordinator thread. Fallback: if direct thread delivery is unavailable, return a coordinator-ready packet in the worker thread starting with `Coordinator handoff - manual relay required` and include the coordinator thread id.

The fallback path is an expected success path. Workers should not try to compensate by forwarding the prompt, creating a new thread, or sending a packet to their own worker thread. If the prompt lacks an exact coordinator thread id or no thread-send tool is available, the worker should end with the manual-relay packet as the final message in the worker thread.

The coordinator is responsible for confirming it received the packet, whether by direct thread delivery or by collecting/pasting a fallback handoff. A fallback packet is not delivered until it is relayed into the coordinator thread.

While a worker is running, the coordinator should stay quiet on that lane. Do not poll, read, summarize, or steer active worker threads unless the worker returns a packet/blocker, the human explicitly asks for inspection, or a clear timeout/recovery step is needed. If direct delivery does not arrive after the worker finishes, the coordinator may perform one collection read to relay a fallback packet; this is receipt recovery, not live monitoring. The coordinator thread should remain available for the human to discuss scope, priorities, and unrelated coordination while workers work independently.

## Decision Routing

Human decisions are coordinator-owned by default.

When a worker packet says `Needs human decision`, `Blocked` on a human gate, `Human judgment needed`, or `Human/manual steps expected`, the worker should return the packet to the coordinator and stop. The worker should not treat its own thread as the approval lane unless the coordinator prompt explicitly delegates that exact human question.

The coordinator then summarizes the options, asks the human in the coordinator thread, records durable decisions in `docs/project/decision-log.md` and the relevant brief/feature spec when needed, and resumes the lane with a new worker prompt or retest request.

If the coordinator delegates a human question to a specialist thread, the prompt must name the exact decision, allowed wording or scope, where to record the answer, and the packet expected afterward. Never delegate collection of secret values.

## Lane-Specific Clarifications

When a specialist lane is active or was recently used, route human follow-up questions about that lane back to the same specialist by default. The coordinator may acknowledge the question and forward it, but should not answer deployment, architecture, analysis, review, UX, or walkthrough clarifications inline unless the answer is purely administrative or the human explicitly asks the coordinator to decide.

When an implementation or inventory lane exists, route additional implementation, inventory, documentation-content, or artifact-update work to that lane by default. The coordinator may update coordination/process records inline, but should not keep changing feature artifacts or inventory content in the coordinator thread unless the human explicitly asks for a one-off inline edit and the coordinator records why it is safe.

Examples:

- Deployment/provider/setup/secrets questions -> deployment guide.
- Stack/API/data-model tradeoffs -> architect.
- User/problem/workflow ambiguity -> analyst.
- Verification/check results -> walkthrough/testing worker.
- Inventory/content corrections after implementation has started -> existing implementation worker or a new worker with explicit file ownership.

## After Human Decisions

When the coordinator receives human decisions for a specialist packet, it records the decisions and returns unresolved specialist work to that role by default.

Do not continue architecture, analysis, UX, deployment, review, or walkthrough work inside the coordinator thread unless the remaining work is trivial and the coordinator says why it is staying inline. For architecture and analysis especially, pass the human decision context back to the same specialist thread, or start a new specialist thread if the old one is unavailable.

Use the smallest useful team. After init, the first planning lane should usually include an architect and may include an analyst when product/domain understanding is fuzzy. For later narrow features, the team is often:

- coordinator
- one implementation worker
- one walkthrough/testing worker

For later feature work, add analyst, architect, reviewer, UX reviewer, or deployment guide only when the feature has a clear need for that role.

## Role Cards

- Architect: `docs/process/roles/architect.md`; agent preset `mamkin-architect`.
- Analyst: `docs/process/roles/analyst.md`; agent preset `mamkin-analyst`.
- Implementation worker: `docs/process/roles/implementation.md`; agent preset `mamkin-worker`.
- Reviewer: `docs/process/roles/reviewer.md`; agent preset `mamkin-reviewer`.
- Walkthrough/test guide: `docs/process/roles/walkthrough.md`; agent preset `mamkin-walkthrough`.
- Deployment guide: `docs/process/roles/deployment.md`; agent preset `mamkin-deployment`.
- UI/UX reviewer: `docs/process/roles/ux.md`; agent preset `mamkin-ux`.
- Custom recurring roles: add role cards under `docs/process/roles/` during init or coordinator-approved setup.

Packet templates are indexed in `docs/process/handoff-packets.md` and split under `docs/process/handoff-packets/`. Naming rules live in `docs/process/naming-conventions.md`.

## Agent Presets

Codex runtime presets live under `.codex/agents/`. They are short launch wrappers for sandbox, reasoning posture, and the handoff return path; they do not replace role cards, packet templates, or feature docs.

When starting a separate Codex thread for a built-in role, use the matching `mamkin-*` preset when the platform supports custom agents. If custom agents are unavailable, include the same role card, packet template, thread name, coordinator thread id, and return-path instructions directly in the prompt.

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
- For parallel write-capable workers, use separate worktrees or explicitly disjoint `Allowed files to edit` ownership.
- Set the worker thread name from `docs/process/naming-conventions.md`, include it in the worker prompt, and rename or request rename if the platform auto-generates a different title.
- After starting a worker, wait for its returned packet instead of monitoring the worker thread.
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
Project:
Role:
Agent preset:
Thread name:
Worker thread id, if known:
Feature/Slice:
Source thread:
Coordinator thread id:
Expected worktree:
Expected branch or commit:
Allowed worktree sharing: separate worktree | disjoint files only | read-only
Read first:
Allowed files to edit:
Do not edit:
Handoff target: coordinator
Handoff return path:
Human decision routing:
Delivery guardrails:
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

For `Thread name`, use `docs/process/naming-conventions.md`. If the platform creates a different title, rename the thread or request rename before treating the worker as properly started. Do not rely on auto-generated titles from the first prompt words.

For `Coordinator thread id`, provide the exact coordinator thread id that should receive direct thread-send packets. For `Worker thread id, if known`, provide the worker's own thread id only as an anti-self-send guard and receipt-recovery handle; it is never the packet delivery target.

For `Human decision routing`, default to `Return human gates to coordinator; do not ask the human directly in this thread`.

For `Handoff return path`, default to `Send the final packet to coordinator thread <id> using thread tools if available; if no thread-send tool is available, return a coordinator-ready packet in this thread starting with Coordinator handoff - manual relay required for coordinator thread <id>`.

For `Delivery guardrails`, include: `Do not forward this prompt, create another handoff thread, or send the packet to this worker thread. If direct delivery is unavailable, emit the manual-relay packet as the final message in this worker thread.`

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

Approval of a verification lane does not approve installing missing tooling. If required local tooling is absent, stop and ask the human to choose: provide an existing endpoint/tool, approve a specific install/setup, use an already available alternative, or defer the check.

After init, the coordinator owns feature-spec and walkthrough creation. The coordinator may write them directly or assign drafting/update tasks, usually after an architect pass for the first project slice. The walkthrough worker normally executes the approved walkthrough; it should not invent acceptance criteria unless the coordinator explicitly asks for missing coverage to be drafted.

## Traceback Contract

Every meaningful feature should leave a clear path:

```text
Project brief -> decision log -> feature spec -> implementation handoff -> tests -> walkthrough -> follow-ups
```

Record durable decisions in `docs/project/decision-log.md`. Record non-blocking discovered work in `docs/follow-ups/`. Do not put temporary thread ownership, live branch status, or secrets in feature specs.

The roadmap should reflect the current durable feature state, not just initial spec creation. If roadmap status and feature docs disagree, update the roadmap before starting the next lane or finalizing a cycle.

## Context Reset Pattern

A context reset is read-only unless the coordinator explicitly assigns doc updates afterward. The reset packet should answer:

- Which current files, docs, reports, commits, environments, or human decisions were read.
- What is currently authoritative.
- What older packet details, assumptions, or generated outputs are obsolete or only historical evidence.
- What external proof shows and what it does not show.
- What action is safe next, or which blocker remains.

Use this pattern instead of arguing from memory in long coordinator threads.

## Coordinator Rollover

Use coordinator rollover when the current coordinator thread is too long, context-heavy, direction has changed, old packets are competing with current sources, or a context reset finds repeated source confusion.

Rollover is a context-management action, not a Git-branching action. Start a fresh coordinator thread from a committed reset baseline when possible. Create a new branch or worktree only for the next write-capable implementation, docs, deployment, or artifact slice when file ownership or review isolation requires it.

Before starting the new coordinator, prepare `docs/process/handoff-packets/coordinator-reset.md` as either a durable project doc under `docs/project/`, a final packet in the old coordinator thread, or both. Prefer committing the reset packet and relevant process/doc updates first so the new coordinator can start from repo truth instead of chat memory.

The reset packet should include source authority, current model, obsolete assumptions, active lanes, dirty repos/worktrees, external proof boundaries, next safe action, and actions the next coordinator must not take yet.

When the human approves rollover and thread-management tools are available, the current coordinator should execute the rollover end-to-end. Do not hand the human a prompt to paste unless thread creation/sending/renaming tools are unavailable or blocked.

During rollover, the current coordinator becomes the outgoing coordinator. Its job is to transfer authority, not to keep coordinating future work. The outgoing coordinator should not start new implementation, review, walkthrough, deployment, research, or Figma/live-validation lanes after rollover starts. It may only prepare the reset packet, create/send/verify the fresh coordinator start, rename/archive itself, and report the result.

There should be only one main coordinator thread after rollover. The fresh coordinator must become the main coordinator once it has received the reset prompt. If title tools are available, either rename/archive the old coordinator before assigning the main coordinator title to the fresh thread, or create the fresh thread with a temporary reset title and then promote it after the old thread is archived. Do not leave two visible coordinator threads that both look active.

Recommended rollover sequence:

1. Old coordinator pauses implementation and live validation.
2. Coordinator or architect prepares a source-grounded reset packet from current files, decisions, packets, and repo state.
3. Human reviews any material decisions or stale-assumption corrections.
4. Commit the reset packet and process/doc updates when Git is available and approved.
5. Create a fresh coordinator thread. Prefer creating a clean new coordinator over forking when fork would carry contaminated context; use fork only when the platform gives a clean enough start or the human requests it.
6. Send the starter prompt below to the fresh coordinator thread, including the reset packet or path to the committed reset doc.
7. Verify the fresh coordinator thread exists and has the starter prompt. If possible, wait for or inspect its first acknowledgement before treating rollover as complete.
8. Rename/archive the old coordinator thread when the platform supports it, using the archived coordinator pattern from `docs/process/naming-conventions.md`.
9. Promote the fresh coordinator to the normal main coordinator title from `docs/process/naming-conventions.md` when title tools are available.
10. Report the new coordinator thread id, baseline commit/doc, old-thread status, title/promotion status, and whether the next write-capable slice needs a branch/worktree.

Fresh coordinator starter prompt:

```text
Read AGENTS.md, docs/process/agent-orchestration.md, docs/process/handoff-packets/coordinator-reset.md, docs/project/decision-log.md, the relevant feature/roadmap docs, and the committed coordinator reset packet/doc listed below.

Start as the fresh coordinator after coordinator rollover. Do not implement, merge, deploy, run live validation, or start write-capable workers yet.

First action: produce a source-grounded architecture restatement from current repo files and the reset packet. Verify repo state and HEAD before reasoning. Treat the old coordinator thread, old packets, and old summaries as historical evidence only.

Reset packet/doc:
<path or packet content>

Required restatement:
- Source authority and exact baseline.
- Current model and active scope.
- Obsolete or unsafe assumptions.
- Active lanes and dirty repos/worktrees.
- External proof boundary.
- Next safe action and must-not-do-next.
- Whether the next write-capable slice needs a branch/worktree.
```

If no thread-management tools are available, write the reset packet locally and return the exact starter prompt as a manual fallback for the human to paste. State that manual start is a fallback because tools were unavailable, not the preferred rollover path. Do not keep trying to repair a drifting coordinator through more inline explanations.

If create/send works but rename/archive is unavailable, the outgoing coordinator must clearly report that old-thread cleanup is manual. It should mark itself historical in its final response and avoid taking more coordination actions. The human or a later coordinator may archive/rename it when tooling becomes available.

## Git And GitHub

- Verify repo state before each implementation or walkthrough.
- In copied projects, treat inherited template Git state and remotes as `TBD`, not as valid project push targets. Do not push project/product commits until the human approves a project-specific remote.
- Do not run multiple write-capable workers on the same worktree/files unless their ownership is explicitly disjoint; prefer separate worktrees for true parallel implementation.
- If git is not initialized, ask before `git init`; creating `.git` may require approval in local agent environments even though the folder is local.
- If staging or committing writes to local Git metadata and the environment asks for approval, request it explicitly and explain that no remote push is implied.
- If no initial commit exists, propose one after docs are adapted.
- Before implementation lanes, prefer a small planning commit so workers start from a stable baseline; if not possible, include the clean/dirty baseline details in each worker prompt.
- A fresh coordinator thread does not require a fresh branch. Branches/worktrees are for write-capable work isolation, not for coordinator context rollover by itself.
- Ask before creating remotes, pushing, creating GitHub issues, milestones, or project boards.
- If GitHub Projects are used, keep issues small enough to map to feature specs or sub-slices.
- Mention expected branch/commit in every worker prompt and final packet.

## Failure Prevention

- Do not run duplicate implementation workers for the same slice.
- Do not let parallel write-capable workers edit the same files or feature spec.
- Do not let old handoff packets or summaries override current source files, manifests, docs, or human corrections.
- Do not treat external proof, generated reports, screenshots, or live checks as broader evidence than the exact thing they verified.
- Do not continue execution from memory after repeated corrections or source confusion; run a context reset first.
- Do not monitor active worker threads unless the worker returns a packet/blocker, the human asks, or timeout recovery is needed.
- Do not test the wrong branch or worktree.
- Do not let workers silently expand scope.
- Do not edit active feature specs during implementation unless explicitly assigned.
- Do not let the coordinator keep implementing inside its own thread after a worker lane exists; use worker packets and retest loops instead.
- Do not hide test gaps behind a confident final sentence.
- Do not paste secrets into docs or chat.
- Do not create production resources without human approval.
