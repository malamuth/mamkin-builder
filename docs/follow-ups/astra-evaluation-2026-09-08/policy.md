# SOURCE: AGENTS.md
# Agent Notes

## Request Routing

- Improve the template itself by editing template files directly; do not run project init. Prompt, role, hook, or reasoning changes also follow `docs/process/prompt-evals.md`.
- Initialize or adapt a copied template with `.agents/skills/mamkin-init/SKILL.md` and `docs/process/init-agent.md`.
- Bootstrap Mamkin on a machine or repository where Mamkin is not discoverable with `.agents/skills/mamkin-bootstrap/SKILL.md`.
- Adopt Mamkin into an existing non-Mamkin repository with `.agents/skills/mamkin-adopt/SKILL.md` and `docs/process/adopt-existing-project.md`.
- Coordinate feature or multi-agent work with `.agents/skills/mamkin-coordinate/SKILL.md` and `docs/process/agent-orchestration.md`.
- Audit coordinator drift with `.agents/skills/mamkin-context-audit/SKILL.md`; run an approved same-thread reset or rollover with the matching Mamkin skill.
- Update a copied project's process layer with `.agents/skills/mamkin-template-sync/SKILL.md`.
- Audit a mature copied project's net-positive process evolution with `.agents/skills/mamkin-project-evolution-audit/SKILL.md` after major syncs or recurring coordination friction.
- Assigned workers read their role card under `docs/process/roles/`, the relevant feature or walkthrough, and only the packet they must return.
- Product context lives in `docs/project/brief.md`, `docs/project/decision-log.md`, relevant `features/*.md`, and `docs/walkthroughs/`.

## Project Commands

Fill these during init once the stack is known. Until then, do not invent commands; report that project commands are not configured.

- Setup/install: TBD
- Run locally: TBD
- Check before handoff: TBD

## Autonomy And Human Gates

- For answer, review, diagnose, audit, or planning requests, inspect relevant material and report; do not implement unless the request asks for changes.
- For change, build, or fix requests, make in-scope local edits and run relevant non-destructive checks without asking first. Reuse unchanged authorization; cite any skill-induced gate. Preserve the objective through corrections. Repeat passing checks only for new evidence. Keep updates concise.
- Stop for human confirmation before external writes or resources, remotes or pushes, paid services, production actions, DNS, public posting, destructive migrations, secrets or production data, scope/privacy/public-behavior tradeoffs, provider or MCP setup, weakening Codex restrictions, or system/global tooling and local service installation.
- In copied projects, inherited Git state and remotes are `TBD` until the human approves a project-specific target. Never use a template remote for project/product pushes.
- If a command needs credentials, use only an explicitly approved local/provider secret path or variable names, and do not print or store secret values.

## Repository Safety And Evidence

- Before implementation, run `pwd`, `git status --short --branch`, and `git rev-parse HEAD`.
- Preserve user changes and explain unexpected dirty state.
- Treat the current project repository and its assigned worktrees as the write boundary. Another repository may be inspected, never mutated. Cross-repository implementation requires a separate human-approved task in that repository.
- In a copied project, an upstream Mamkin candidate is proposal-only. Project approval never authorizes `mamkin-builder` changes or a template commit manufactured for the project's own sync.
- Current human decisions and current repo sources outrank old packets, summaries, memory, generated reports, screenshots, and external checks. State the narrow proof boundary of external evidence.
- Multiple write-capable agents must use separate worktrees or explicitly disjoint file ownership.
- Use `docs/process/execution-lane-routing.md` to choose between a same-task subagent and a separate Codex task, and before running two independent work tracks.
- Keep reusable process in `docs/process/`; keep project plans and state in `docs/project/`, `features/`, `docs/walkthroughs/`, or `docs/follow-ups/`.
- Keep active feature specs stable during implementation unless spec editing is explicitly assigned.
- Before feature writes, require the Git delivery contract in `docs/process/git-delivery.md`; feature branches are the default, and the coordinator owns integration and cleanup.
- Run relevant validation before completion, or report what could not be run and the next best check.
- Project-local `.codex` config, hooks, rules, and presets load only when the project is trusted; changed hooks may need review. Runtime permissions can be broader than preset defaults, but they do not override these human gates or file ownership.

## Worker Handoff Contract

- The coordinator owns human decisions unless the worker prompt delegates one exact question.
- Every separate-task worker prompt must provide the coordinator thread id and exact handoff path. Use direct thread send when available; otherwise return one final packet beginning `Coordinator handoff - manual relay required for coordinator thread <id>`.
- A subagent prompt must name its parent lane owner. The subagent returns one result or role packet to that parent; the parent owns any coordinator handoff.
- Never send a packet to the worker's own thread, forward the coordinator prompt, or create a duplicate handoff task. Return once, then stop.
- Independent work tracks use separate Codex tasks. Bounded delegation may use subagents only under `docs/process/execution-lane-routing.md`; implementation and acceptance must never be performed by the same subagent.


# SOURCE: docs/process/agent-orchestration.md
# Agent Orchestration

This is the coordinator manual after init. Workers do not read it by default; they receive `AGENTS.md`, one role card, the relevant feature or walkthrough, and one return packet.

## Scope And Conditional Reading

Keep live project state in `docs/project/`, `features/`, `docs/walkthroughs/`, and `docs/follow-ups/`. Edit this manual only for reusable coordination policy.

The coordinator reads:

- This manual plus the current brief, decision log, roadmap, and relevant feature material.
- `docs/process/execution-lane-routing.md` only before delegation, subagent use, or two-track admission.
- `docs/process/model-routing.md` before selecting a delegated worker's model, effort, or profile preset.
- `docs/process/git-delivery.md` when activating a write-capable feature, assigning its implementation lane, or closing it out.
- `docs/process/thread-operations.md` only when creating, receiving from, or recovering a separate task.
- `docs/process/naming-conventions.md` only when naming or renaming a durable task or follow-up document.
- The one packet file needed for the current handoff. Use `docs/process/handoff-packets.md` only when the correct packet is unclear.
- `docs/process/context-health-audit.md` only when context drift or source confusion is suspected.

## Follow-Through And Communication

- Reuse explicit authorization while its scope and conditions remain unchanged. Complete authorized preparation before presenting a human gate; ask only for missing decisions that materially affect the outcome.
- Treat mid-task corrections as steering: preserve completed work and the original objective unless the human cancels or replaces it. Answer side questions, then resume authorized work.
- If a skill causes a pause, cite its exact file and instruction, distinguish a requirement from an inferred precaution, and check whether current human authorization already resolves it. User instructions outrank skill guidance within runtime restrictions.
- After required checks pass, broaden or repeat them only for new changes, failures, or unresolved risks. Avoid tests that merely mirror a reversible, low-impact edit.
- Keep user updates concise and concrete; preserve required evidence in role packets without repeating process rules in every update.

## Source Authority And Reset

When facts conflict, use:

1. Current human decisions and durable decision records.
2. Current repo sources, manifests, project docs, feature specs, walkthroughs, and runbooks at the named state.
3. Generated reports or external proof from a named branch, commit, environment, or target.
4. Old packets, summaries, screenshots, and memory.

External proof establishes only the observed fact, not broader architecture or merge readiness. Mark conflicting old packet details obsolete.

Run a source-grounded reset when the coordinator repeats a corrected fact, cannot cite the source behind an important claim, treats old context as authority, or sees source and generated/external evidence disagree. Use `mamkin-context-audit`, `mamkin-context-reset`, or approved rollover for more than a small inline reread.

Require a short architecture restatement before a merge, external validation, deployment, or routing decision only when at least one applies:

- Source ownership or authority is disputed.
- Two tracks, repositories, or components must be integrated.
- The change affects a shared contract, schema, migration, auth/security boundary, or deployment topology.
- Generated artifacts or external evidence materially support the decision.

The restatement names the exact state, authoritative sources, scope, evidence limits, obsolete assumptions, and unresolved owner. If those cannot be named without guessing, reset or route to the architect.

## Team And Architecture Routing

Use the smallest useful team. Analyst resolves user, workflow, business-rule, or domain ambiguity. Architect resolves structure, boundaries, tradeoffs, and slicing.

Use an architect before implementation when any applies:

- The first slice lacks an accepted feature spec or equivalent bounded brief.
- The change alters a shared data model, schema, migration, auth/security boundary, API/public contract, external integration, provider, or deployment topology.
- Ownership spans multiple components or tracks, or integration order is unclear.
- A material cost, privacy, recoverability, or long-lived architecture tradeoff remains open.
- Current sources conflict about architecture or ownership.

Skip the architect when all apply:

- Acceptance criteria, allowed ownership, and validation are already explicit.
- One bounded owner can complete the slice without changing shared contracts, migrations, security boundaries, or external topology.
- Existing decisions/specs settle the relevant architecture.

Designer, UX, reviewer, walkthrough, and deployment roles are conditional:

- Designer: approved design artifacts or visual-system work.
- UX: user flow, hierarchy, states, accessibility, or responsive fit.
- Reviewer: correctness, security, migration, API-contract, regression, or test risk merits a second engineering read.
- Walkthrough: acceptance verification after implementation; always a different agent from implementation.
- Deployment: environment, provider, release, secrets path, or production readiness.

Built-in role cards live under `docs/process/roles/`. Choose the role first, then select a reasoning profile from observable risk signals in `model-routing.md` and use its access-specific launch preset. Existing role presets remain compatibility fallbacks; use one only when it meets or exceeds the selected risk floor. Never silently downgrade because a model or preset is unavailable.

## Feature Cycle

1. **Orient:** verify repo state; read current project sources; triage unresolved follow-ups.
2. **Specify:** use analyst or architect only under the triggers above. Produce an accepted feature spec or equivalent brief plus walkthrough coverage.
3. **Baseline:** prefer a clean commit containing accepted planning state. Otherwise record the exact branch, commit, and dirty-state boundary.
4. **Delivery:** declare the Git delivery contract. Use a named feature branch by default; obtain any external closeout authority for that exact branch separately.
5. **Route:** choose subagent or separate task with `execution-lane-routing.md`; admit at most tracks `A` and `B`.
6. **Implement:** one owner per slice; preserve feature-spec stability unless editing it is assigned.
7. **Review:** add only when the risk triggers above apply.
8. **Verify:** a different agent runs approved checks and applicable walkthrough scenarios against the exact committed state.
9. **Integrate:** the coordinator follows `git-delivery.md`; for two tracks, integrate in order and run combined checks before `Integration-verified`.
10. **Close:** finish authorized Git closeout, reconcile roadmap/decisions/follow-ups, report validation and retained state, and name the next action.

Update roadmap state at cycle transitions rather than repeating live state in process docs.

## Lane And Decision Routing

Separate-task workers return one packet to the coordinator. Subagents return once to their named parent, which inspects the result and owns any coordinator handoff. Workers do not hand work directly to peers or start follow-up lanes unless explicitly delegated.

Human decisions remain coordinator-owned unless a worker prompt delegates one exact question. On a human gate, the worker returns a blocker; the coordinator presents options, obtains the decision, records it when durable, and resumes the same role when practical. Never delegate collection of secret values.

Route substantive follow-ups to the active or most recent relevant owner:

- User/domain ambiguity -> analyst.
- Data/API/architecture tradeoff -> architect.
- Implementation or artifact correction -> implementation owner.
- Verification result -> walkthrough.
- Provider/setup/release question -> deployment.

The coordinator may handle an administrative answer or a small process-record edit inline. It should not take over an established specialist's substantive work merely to avoid a return handoff.

## Worker Prompt Contract

Every worker prompt includes this core:

```text
Role:
Reasoning profile: economy | balanced | deep | critical
Profile trigger and risk floor:
Agent preset / model / effort:
Access posture: read-only | workspace-write
Escalation conditions:
Goal:
Success criteria:
Required evidence and source authority:
Scope and allowed files:
Human and permission boundaries:
Validation required:
Output packet:
Stop and fallback rules:
Execution mode: separate task | subagent
Assigned return destination:
Read first:
```

Add only applicable extensions.

### Separate-Task Extension

```text
Agent preset:
Thread name:
Coordinator thread id:
Worker thread id, if known:
Expected worktree:
Expected branch or commit:
Handoff return path:
```

Read `docs/process/thread-operations.md` and `docs/process/naming-conventions.md` before filling this extension.

### Subagent Extension

```text
Parent lane owner:
Subagents: not allowed
Expected worktree:
Files or surfaces owned:
Changed-files report required: yes | not applicable
```

The parent owns validation and any coordinator delivery.

### Write-Capable Extension

```text
Allowed worktree sharing: separate worktree | disjoint files only
Do not edit:
```

Use separate worktrees or provably disjoint ownership for concurrent writers.

### Parallel-Track Extension

```text
Parallel track: A | B
Common base commit:
Integration target:
Shared surfaces excluded:
Cross-track assumptions:
Integration order:
Combined checks:
```

Do not include parallel fields for a single-track assignment. `execution-lane-routing.md` owns admission rules.

Keep `Read first` to `AGENTS.md`, one role card, one feature spec or walkthrough, one packet, and only necessary project sources. Add lane routing only when delegation or parallelism requires it.

Lead with the observable result. `Stop and fallback rules` requires one return to the assigned destination and a blocker when sources are unavailable, a human gate is reached, or success criteria cannot be met.

## Follow-Up Triage

Classify discovered work before routing:

- **Current feature:** required for stated value, acceptance, or a defect in changed behavior.
- **Optional current follow-up:** small and low risk; do only when it will not destabilize the lane.
- **Future feature:** belongs in a roadmap candidate or future spec.
- **Deferred note:** real but not yet scoped; keep in `docs/follow-ups/`.

Scope, privacy, public behavior, or product-direction changes return to the coordinator before implementation. Before an architect pass, identify which unresolved follow-ups are in, out, or open for recommendation.

## Quality And Completion

The coordinator verifies:

- Current sources and returned evidence agree.
- Expected ownership and changed files match.
- Required checks ran, or the gap and next best check are explicit.
- Implementation and final acceptance were performed by different agents.
- Parallel tracks are reported separately from integrated-state verification.
- Roadmap, decisions, walkthrough results, and follow-ups are reconciled.
- The Git delivery contract was followed; `Merge-ready` is not reported as `Delivered` before integration and required cleanup.
- Final status is `delivered`, `ready for Git closeout`, `merge-ready`, `verified with follow-ups`, `blocked`, or `not ready`.

Project commands and human gates come from `AGENTS.md`; do not duplicate them here. Git or external writes still require the applicable human authorization. Context audit/reset/rollover details live in their focused skills and process docs.


# SOURCE: docs/process/model-routing.md
# Adaptive Model Routing

Use this protocol before launching delegated work. Choose role, reasoning profile, and access posture independently. The role owns the responsibility and packet; the profile owns model effort; access owns the sandbox. Task size alone does not select a stronger profile.

## Profiles

| Profile | Model and effort | Default use |
| --- | --- | --- |
| Economy | `gpt-5.6-terra` / `medium` | Bounded read-only inventory, extraction, classification, or mechanical verification with a deterministic oracle. Luna/low remains an experiment candidate after failing the current same-case quality gate. |
| Balanced | `gpt-5.6-terra` / `medium` | Reversible, well-specified implementation, deployment, testing, and ordinary analysis. |
| Deep | `gpt-6-astra` / `high` | Conflicting sources, architecture tradeoffs, shared contracts, cross-component work, unknown root cause, nondeterministic validation, or material product judgment. |
| Critical | `gpt-6-astra` / `xhigh` | Security/auth boundaries, payments, production data or incidents, destructive migrations, irreversible external state, or concurrency correctness. |

The coordinator uses `gpt-6-astra` / `medium`. Analysis, architecture, review, walkthrough, design, and UX compatibility presets explicitly use Astra/high; they cannot substitute for Critical/xhigh. Worker and deployment compatibility presets remain Terra/medium. Select by risk floor, not by role name.

These Astra defaults are a user-directed pilot dated 2026-09-08, with comparative execution evidence pending in `prompt-evals.md`. Preserve effort during the model comparison; evaluate any effort reduction separately. Existing tasks and already-loaded presets may retain earlier settings: verify the effective model and effort at launch, preferably in a fresh task. Do not change user-level configuration or silently substitute a model when Astra is unavailable.

Never select `max` automatically. It requires a human choice or accepted same-case evidence that `xhigh` is insufficient. The selector does not emit a `max` preset; an approved exceptional launch is runtime-specific and must be recorded in the assignment and experiment log.

## Deterministic Selection

Classify observable signals, then run:

```bash
python3 scripts/select_model_profile.py \
  --role reviewer \
  --access read-only \
  --signal shared-contract
```

Critical signals establish a `critical` floor; deep signals establish a `deep` floor. Economy requires read-only access plus every configured economy requirement. Everything else starts balanced. A requested profile may raise the result but never lower its risk floor.

The selector returns the exact profile preset. Profile presets deliberately contain no role identity: the worker prompt must still name one role card and packet. Use an existing role preset only as a compatibility fallback when it meets or exceeds the selected floor. If the selected preset or model is unavailable, stop and report it; never silently downgrade critical or deep work.

## Escalation And De-escalation

Escalate only on new evidence:

- two focused attempts fail without explaining the cause;
- requirements or authoritative sources conflict;
- scope crosses a component or shared contract;
- the validation oracle becomes nondeterministic or insufficient; or
- a critical signal appears.

Return the current profile, requested profile, trigger, evidence, and next bounded action. The coordinator decides whether to relaunch; workers do not silently change models. Do not escalate merely because a task is long or a test is slow.

After architecture or diagnosis resolves the uncertainty, route the next bounded implementation independently and allow a lower profile when its remaining risk floor permits it. Acceptance selects its own profile and remains independent from implementation.

## Evaluation

Use the model-routing cases in `evals/mamkin-prompt-cases.json` and the hard quality gate in `evals/mamkin-role-model-matrix.json`. Compare adjacent profiles on the same state. Record success, missed or unsupported findings, permissions, validation, handoff, correction turns, latency, tokens, tool calls, and cost when available. A cheaper profile is accepted only when every hard dimension passes.


# SOURCE: docs/process/execution-lane-routing.md
# Execution Lane Routing

Use this file to choose between a same-task subagent and a separate Codex task, and to admit at most two independent work tracks. A Codex task and thread are the same durable, user-visible lane in this process.

## Core Boundary

- A separate task owns an independent workstream.
- A subagent performs bounded delegation inside its parent task.
- Prefer a subagent when every subagent condition below passes. Use a separate task when any separate-task trigger applies.
- The parent task remains accountable for subagent scope, evidence, edits, and validation.
- One subagent must not both implement a change and provide its acceptance verdict.
- Git delivery is orthogonal to task routing: `docs/process/git-delivery.md` chooses the branch, worktree, integration path, merge method, authority, and closeout owner before a write-capable feature starts.
- A repository boundary is also a task boundary for writes. Work targeting another Git repository requires a separate human-approved task with that repository as project context; a subagent or adjacent checkout does not extend the parent task's write authority. Explicitly assigned worktrees of the current repository remain governed by the normal lane and Git-delivery rules.

## Use A Subagent Only When Every Condition Passes

- The assignment is bounded enough to finish in one returned result or packet.
- It needs no direct human conversation, approval, secret, paid service, production action, or external mutation.
- It does not need a durable user-visible lane, independent recovery history, or coordinator rollover survival.
- It uses the parent's current worktree; it does not need its own branch or worktree.
- Its ownership is read-only or explicitly disjoint from every concurrent writer.
- The parent can inspect the result immediately and remains responsible for the final decision.
- A write-capable subagent stays inside files already owned by the parent lane, reports every changed file, and leaves validation to the parent as the final quality gate.

Good subagent work includes repository exploration, focused research, diff review, test-failure triage, drafting a bounded spec section, a narrow disjoint-file edit, or deterministic local verification against a named state.

## Use A Separate Task When Any Trigger Applies

- The assignment owns an independent acceptance outcome that can pause, resume, or be prioritized separately.
- It may need direct human clarification, approval, or follow-up after the parent moves on.
- It owns a branch, worktree, external target, or durable specialist responsibility.
- It would write to a different Git repository, including an upstream template or reusable-tool repository.
- Write ownership spans multiple components or affects a shared API, schema, migration, auth/security boundary, lockfile, generated source, global configuration, or external integration.
- The work cannot be bounded to one prompt with explicit allowed files, observable success criteria, and a known validation path.
- Verification needs manual judgment, interactive UI, accounts, secrets, external systems, environment setup, or a defect/retest cycle.
- The result needs a durable handoff packet, user-visible progress, or clean context isolated from the coordinator.
- Source ownership overlaps another active writer or cannot be proved disjoint.

Architecture, implementation, walkthrough, deployment, or specialist work uses a separate task only when one of these triggers applies. A bounded pass in any role may be a subagent when every subagent condition passes and acceptance remains independently owned.

A feature branch does not by itself require a separate task. One write-capable lane may use the current worktree on the declared branch; concurrent or independently recoverable writers use separate worktrees. Direct-to-base feature work is not a routing shortcut.

## Prompt Declaration

Every delegated prompt declares:

```text
Execution mode: separate task | subagent
Assigned return destination:
```

For a subagent, add `Parent lane owner` and `Subagents: not allowed`; nested subagents are not part of this model. For a separate task, add the coordinator id, durable return path, worktree, and branch/commit boundary. Add `Subagents: allowed` only when the separate-task owner may create bounded helpers under this policy; it never authorizes another independent workstream or delegated human decisions.

Add `Parallel track: A | B` and the full parallel extension only for admitted two-track work. Do not add parallel fields to a single-track prompt.

A separate-task worker returns its role packet to the project coordinator. A subagent returns once to `Parent lane owner`; the parent checks the result and owns any later coordinator packet.

## Two-Track Admission

Parallel mode is optional and limited to tracks `A` and `B`. A third independent track waits until one active track reaches a terminal state. Both tracks remain under one project coordinator. The cap applies to independent workstreams; bounded subagents remain internal to their parent track and do not become additional tracks.

Before launch, the coordinator records these facts in the two worker prompts:

```text
Parallel track: A | B
Common base commit:
Integration target:
Expected worktree:
Expected branch:
Allowed files or surfaces:
Shared surfaces excluded:
Cross-track assumptions:
Integration order:
```

Admit both tracks only when all are true:

- Each has a feature spec or equivalent bounded brief and independent acceptance criteria.
- Neither depends on the other's unintegrated output.
- File ownership is disjoint, or each write-capable track has a separate worktree.
- They do not independently change the same schema, migration sequence, API contract, lockfile, generated source, global configuration, shared fixture, or external environment.
- The coordinator owns shared project-control files such as the roadmap and decision log unless one track receives explicit exclusive ownership.
- The common base, integration target, integration order, and combined checks are known.

If any condition fails or cannot be proved, serialize the tracks or route the boundary question to the architect. A blocked track does not block the other unless a shared assumption changes.

## Track Completion And Integration

- Packets may return in either order; tag every packet with its track.
- Do not poll active tracks. Continue on returned packets, blockers, human requests, or explicit recovery.
- A track that passes its own walkthrough is `Track-ready`, not yet `Integration-verified`.
- Integrate in the declared order, inspect conflicts and changed assumptions, then run the combined checks named at admission.
- Repeat any walkthrough scenario affected by the combined state.
- The coordinator reports each track result and the integrated result separately.

## Acceptance Separation

Implementation and acceptance use different agents. Either of these shapes is valid:

- Separate implementation task -> separate walkthrough task.
- Separate implementation task -> bounded walkthrough subagent, only when verification is deterministic, local, non-interactive, uses a named commit, and needs no retest cycle.
- Coordinator-owned bounded edit meeting every subagent condition -> implementation subagent -> different bounded verification subagent.

Use a separate walkthrough task whenever any separate-task trigger applies. The implementation agent, including any implementation subagent, never issues the final acceptance verdict for its own changes.


# SOURCE: docs/process/git-delivery.md
# Git Delivery

Use this protocol for every write-capable feature or substantive slice. It owns the path from accepted planning baseline to clean integrated repository state. Project commands and external-action gates still come from `AGENTS.md`.

## Delivery Contract

Before product implementation, the coordinator declares this contract. When an accepted spec lacks it, resolve missing choices, create/switch to the named branch from the clean base, and record the contract as the first branch change before product code. Do not edit the base merely to add the contract.

```text
Base branch:
Feature branch:
Worktree: current | separate
Delivery mode: feature branch | direct-to-base exception
Direct-to-base rationale and approval: N/A | exact decision
Integration path: pull request | local
Merge method: merge commit | squash | fast-forward
Remote and base target: <remote>/<base branch>
Local Git authority: branch + commit | working tree only
External Git authority: none | push branch + open PR | full closeout
Remote branch cleanup: retain | delete after verified integration
Closeout owner: coordinator
```

Use `feature branch` by default, named `codex/fNN-short-scope`. Create it from a clean accepted planning baseline before product writes. A separate write-capable task normally owns a separate worktree on that branch; a single same-task lane may use the current worktree when no other writer overlaps.

`direct-to-base exception` is allowed only when all are true:

- the change is a small administrative or process-only edit, not feature behavior;
- it changes no shared API, schema, migration, dependency/lockfile, generated source, security boundary, or production configuration;
- no other writer is active and the base is clean;
- the human explicitly approves the exception.

An urgent feature or hotfix still uses a branch unless the human approves a named exception after seeing the risk.

## Existing Dirty-Base Recovery

If feature writes already exist on the base before a contract is declared, stop new writes and inventory the exact dirty state. Do not stash, reset, discard, or silently move a mixed worktree.

- When every dirty path belongs to one feature and the human confirms that boundary, create the named feature branch from the current base while preserving the worktree, then commit and validate there.
- When adoption/process work, unrelated user edits, or multiple features are mixed, present a path-level ownership and recovery plan first. Separate commits or worktrees only when provenance is clear; otherwise keep the state untouched and ask for the smallest ownership decision.
- Record the original base commit and dirty boundary. Recovery does not retroactively authorize external Git actions or make existing changes accepted.

## Authority

Local branching and commits may proceed when the delivery contract grants `branch + commit`; runtime approval may still be required for `.git` writes. Workers never infer authority to push, create a PR, merge externally, or delete a remote branch.

At kickoff, the coordinator may ask once for exact external authority covering the named feature branch, remote/base target, integration path, merge method, and conditional cleanup. `full closeout` authorizes only that lifecycle after required review, walkthrough, and checks pass. A changed branch, remote/base, path, method, failed gate, conflict, or expanded scope invalidates that authorization and returns to the human.

## Implementation And Verification

- The implementation owner works only on the declared feature branch/worktree and makes focused local commits when authorized.
- Before handoff, intended changes should be committed and the worktree clean. If commits are not authorized, report `working tree only`; the result cannot be `Merge-ready` until an exact committed state exists.
- Reviewer and walkthrough inspect the declared branch and exact commit. They do not merge, push, or clean branches.
- A new implementation commit invalidates an older acceptance verdict; retest the affected scope.
- Do not rebase an accepted commit during closeout. If rebasing is required, treat the rebased tip as a new implementation state and repeat affected acceptance before integration.
- Two tracks remain `Track-ready` until integration order and combined checks pass on the integrated state.

## Coordinator Closeout

After acceptance, the coordinator owns closeout:

1. Confirm the accepted commit equals the local feature-branch tip, any existing remote feature tip has no unaccepted commits, the feature worktree is clean, the intended diff is bounded, and authority still matches the exact remote/base/path/method.
2. Update or compare the base without discarding work. Stop on drift, conflicts, unrelated dirty state, or failed required checks.
3. For `local`, integrate by the declared merge method, run required post-integration checks, then push the base when authorized.
4. For `pull request`, push the feature branch and open/update the PR against the exact remote/base, wait for required checks or review, merge by the declared method, then verify the resulting remote base. Do not locally integrate first.
5. Run combined or post-integration checks against the resulting base whenever integration changes the accepted state or the contract requires them.
6. Remove a feature worktree only when clean. Delete a local branch only after integration is verified: the accepted commit is reachable from the base for merge/fast-forward, or the recorded squash result contains the intended accepted diff. Immediately before remote branch deletion, fetch/compare its tip again; stop if it contains any commit not accepted and integrated. Delete it only when explicitly authorized and remote integration is verified.
7. Verify the base is checked out where appropriate, clean, and synchronized with its approved remote. Report retained branches/worktrees and why.

If external authority is missing, stop once the feature is `Ready for Git closeout`, present the exact pending actions as one approval request, and resume closeout after approval. Do not call a feature `Delivered` merely because implementation or walkthrough finished.

## Completion States

- `Ready for walkthrough`: committed implementation awaits independent acceptance.
- `Merge-ready`: accepted commit is ready to integrate; Git closeout is incomplete.
- `Ready for Git closeout`: acceptance passed but required integration authority is missing.
- `Delivered`: accepted changes are integrated, required remote updates are verified, cleanup matches the contract, and the base state is clean.
- `Blocked`: state, authority, conflict, validation, or ownership prevents safe progress.

Rollback before integration is branch/worktree removal after preserving any requested evidence. After integration, use a normal revert or project-approved recovery path; never rewrite shared history unless the human explicitly approves the exact destructive action.


# SOURCE: docs/process/roles/implementation.md
# Implementation Role Card

You are the implementation worker for one bounded slice. Your job is to make the assigned code or doc change, verify it with focused checks, and return a complete handoff to the destination assigned by the execution mode.

## Read First

- `AGENTS.md`
- this role card
- `docs/process/execution-lane-routing.md` when the prompt allows subagents or assigns a parallel track
- relevant feature spec
- relevant project docs named by the coordinator
- `docs/process/naming-conventions.md` if creating or renaming docs
- `docs/process/handoff-packets/implementation.md`

## Responsibilities

- Verify `pwd`, `git status --short --branch`, and `git rev-parse HEAD` before editing.
- Confirm the prompt declares execution mode, parent owner, subagent permission, and parallel track. Return a blocker when the declared mode violates `docs/process/execution-lane-routing.md`.
- Confirm the worktree and branch match the feature's Git delivery contract. Do not start feature writes on the base branch unless the contract records an approved direct-to-base exception.
- Implement only the assigned slice.
- Use the coordinator-provided feature spec or scoped brief as the implementation boundary.
- Follow existing codebase patterns and local docs.
- Run focused automated checks.
- Make focused local commits before handoff when the delivery contract grants `branch + commit`; otherwise report `working tree only` and do not claim merge readiness.
- Report generated churn separately from source changes.
- Stop and call the coordinator when human input, secrets, external services, system/global tooling, local services, destructive changes, wrong worktree, wrong branch, or duplicate ownership is involved.
- Route human decisions through the coordinator unless explicitly delegated.
- Return final work under the Worker Handoff Contract: to the coordinator from a separate task, or to the named parent lane owner from a subagent.

## Do Not

- Start adjacent feature work.
- Create subagents unless the prompt says `Subagents: allowed`; allowed helpers remain bounded by `docs/process/execution-lane-routing.md` and this lane's file ownership.
- Edit active feature specs unless explicitly assigned.
- Draft or update walkthroughs unless explicitly assigned.
- Touch production systems, secrets, billing, DNS, or external resources.
- Never merge to the base, push, open or merge a PR, delete branches, or remove worktrees. Git closeout remains coordinator-owned.
- Hide tests that were not run.

## Return

Use `docs/process/handoff-packets/implementation.md`.
A separate task returns the packet to the coordinator; a subagent returns it to the named parent lane owner.
Follow the Worker Handoff Contract in `AGENTS.md`. Return one packet, then stop.


# SOURCE: docs/process/handoff-packets/implementation.md
# Implementation Handoff

```text
Status: Ready for walkthrough | Needs review | Blocked
Role: implementation
Reasoning profile used:
Model and effort used:
Profile trigger or escalation evidence:
Execution mode: separate task | subagent
Parent lane owner:
Coordinator thread id:
Return path used: Parent lane return | Direct thread send | Manual relay required
Feature/Slice:
Parallel track: none | A | B
Delivery mode:
Worktree:
Branch:
Base commit:
Final commit or HEAD:
Commit state: clean committed state | working tree only
External Git actions performed: none
Cross-track assumptions changed: No | Yes, describe
Changed files:
Generated churn:
Migrations:
Environment variables:
Automated checks run:
Checks not run:
Manual smoke performed:
Known risks:
Retest focus:
Integration checks required:
Human/manual steps expected:
Git closeout remaining:
Secrets or live systems touched: No | Yes, describe without values
```


# SOURCE: docs/process/roles/reviewer.md
# Reviewer Role Card

You are the reviewer for a completed implementation slice. Your job is to find blocking correctness, security, migration, contract, regression, or test issues before walkthrough or merge.

## Read First

- `AGENTS.md`
- this role card
- relevant feature spec
- implementation handoff or diff base
- `docs/process/handoff-packets/reviewer.md`

## Responsibilities

- Review behavioral regressions, tests, data changes, auth boundaries, API contracts, generated churn, and risky migrations.
- Lead with findings ordered by severity. Do not put praise or a general summary before findings.
- For every finding, provide severity, the tightest file/line or symbol reference available, the concrete failure mode, supporting evidence, and the smallest safe correction.
- Distinguish a correctness or acceptance defect from an optional improvement. Do not inflate style preferences into blockers.
- Mark evidence as executed, statically inspected, or unverified. Do not imply a check ran when it did not.
- Return `No blocking findings` only when no blocking issue is found.
- Call the coordinator when acceptance risk or review scope is unclear.
- Route human decisions through the coordinator unless explicitly delegated.
- Return final work under the Worker Handoff Contract: to the coordinator from a separate task, or to the named parent lane owner from a subagent.

## Do Not

- Rewrite implementation while reviewing unless explicitly assigned.
- Request broad refactors unrelated to the feature.
- Ignore missing tests for changed behavior.
- Report a speculative risk as a proven defect.

## Return

Use `docs/process/handoff-packets/reviewer.md`.
Follow the Worker Handoff Contract in `AGENTS.md`. Return one packet, then stop.


# SOURCE: docs/process/handoff-packets/reviewer.md
# Reviewer Packet

```text
Status: Findings | No blocking findings
Role: reviewer
Reasoning profile used:
Model and effort used:
Profile trigger or escalation evidence:
Execution mode: separate task | subagent
Parent lane owner:
Coordinator thread id:
Return path used: Parent lane return | Direct thread send | Manual relay required
Feature/Slice:
Parallel track: none | A | B
Reviewed diff:
Findings:
  - Severity:
    Location:
    Failure mode:
    Evidence: Executed | Static inspection | Unverified
    Smallest safe correction:
Checks considered:
Checks executed:
Optional improvements:
Residual risks:
Recommended next action:
```
