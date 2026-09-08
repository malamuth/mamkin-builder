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

The coordinator uses `gpt-5.6-sol` / `medium`: the Astra coordinator pilot did not clear the strict policy-response gate on 2026-09-08. Re-evaluate before activating Astra for coordination. Analysis, architecture, review, walkthrough, design, and UX compatibility presets explicitly use Astra/high; they cannot substitute for Critical/xhigh. Worker and deployment compatibility presets remain Terra/medium. Select by risk floor, not by role name.

The remaining Astra specialist defaults are a user-directed pilot dated 2026-09-08. Bounded fixture evidence and its limits are recorded in `prompt-evals.md`; it does not establish real-project specialist quality. Preserve effort during the model comparison; evaluate any effort reduction separately. Existing tasks and already-loaded presets may retain earlier settings: verify the effective model and effort at launch, preferably in a fresh task. Do not change user-level configuration or silently substitute a model when Astra is unavailable.

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


# SOURCE: docs/process/project-evolution-audit.md
# Mamkin Project Evolution Audit

Use this protocol to decide which current Mamkin mechanics would materially improve a mature copied project. Run it when a major template update is available, after a sync review, or after an applied sync; never run it as part of the sync mutation itself.

## Inputs And Proof Boundary

- Mature project worktree and current Mamkin template worktree.
- `.mamkin/template-version.json` and ownership metadata when available.
- Deterministic inventory from `scripts/audit_mamkin_evolution.py`.
- Current project brief, decision and learning logs, follow-ups, repeated artifacts, validation commands, hooks, rules, presets, skills, and relevant recent Git history.

Current project sources outrank old packets or memories. Decision and surprise/lesson logs are discovery inputs, not self-proving instructions. Git history, headings, status signals, and text counts show possible recurrence or lifecycle state, not root cause or current authority. The inventory never proves usefulness.

## Audit Sequence

1. Verify both worktrees and record branch, HEAD, and dirty state. Continue read-only when dirty; do not ask to clean unrelated work.
2. Establish the project's recorded template baseline and current template HEAD. State when the baseline is missing or unavailable in the template repo.
3. Run the inventory script from the current template.
4. Classify candidates:
   - **Upgrade gap:** a current template capability is absent, partial, or inactive.
   - **Project leverage:** project scale, specialized knowledge, custom workflows, or repeated friction creates a project-specific opportunity.
   - **Redundancy:** an old project mechanism duplicates or conflicts with the current protocol.
   - **No-fit:** a capability is absent but has no demonstrated project value.
5. Read only the project evidence needed to evaluate plausible candidates.
6. Score, filter, and render the audit packet in the response. Do not write the packet or apply recommendations.

A dirty or unverified template may support capability assessment, but it is not an executable sync source. Make the next sync action conditional on a committed, clean template whose reviewed HEAD is verified against the intended upstream or explicitly approved as local-only.

## Evidence Gate

A recommendation needs at least one:

- Two or more concrete occurrences of the same friction or manual workaround.
- One high-impact safety, recoverability, ownership, or external-action gap.
- A deterministic prerequisite missing from a project with multiple prior process updates or substantial project-specific process customization.
- A measured prompt, latency, validation, or handoff regression that the mechanic directly addresses.

Do not recommend a hook, model change, new role, extra document, or automation because it exists upstream. Name exact evidence and its source.

## Project-Native Capability Pass

Inspect bounded current evidence: decision logs, surprise/lesson/incident sections, accepted follow-ups, repeated task artifacts, existing project skills and references, deterministic checks, and relevant history. Verify every candidate against current human decisions and current project sources; reject stale or contradicted log entries.

Choose the smallest primary action:

1. Keep the knowledge in its current source.
2. Update or consolidate an existing skill, reference, role, or process source.
3. Add a deterministic validator/check when the rule is mechanically testable.
4. Create a project-local skill only for a distinct recurring invocation.
5. Propose an upstream Mamkin improvement only when the mechanism is project-agnostic and evidenced beyond one project's domain details.
6. Merge, retire, or mark legacy a redundant capability.

Do not recommend several surfaces for the same lesson unless each has a separate job. Prefer references for detailed domain knowledge and keep skill entrypoints concise. A project-native recommendation remains owned by that project and must not leak project names, private targets, domain rules, or identifiers into Mamkin.

### Upstream Proposal Boundary

`Propose upstream` produces a proposal packet, never a cross-repository implementation. The copied-project task may name the generic problem, anonymized evidence, candidate Mamkin surfaces, success criteria, and risks. It must not edit, branch, stage, commit, or push the template repository, even when that checkout is locally available or the human says to proceed with the project plan.

Implementation requires a separate human-approved task whose project context and Git root are `mamkin-builder`. Approval to create that task authorizes reassessment only; implementation also requires an explicit starter scope or later human decision. The task starts from current Mamkin sources, independently evaluates the proposal, and owns its own delivery contract. It must not treat a patch or commit manufactured by the copied-project task as trusted input. Return to the copied project only after the accepted Mamkin change is published to the intended upstream, or through an exceptional pre-existing local-only source whose provenance and exact commit the human approves. The copied-project task cannot create that exception for itself.

## Profitability Score

Score each candidate:

```text
Benefit = recurrence (0-3) + time/token saving (0-3) + risk reduction (0-3) + project fit/confidence (0-2)
Cost = adoption effort (0-3) + ongoing maintenance (0-3)
Net value = Benefit - Cost
```

Classify:

- **Adopt now:** evidence gate passes, net value at least `6`, success is measurable, and rollback is clear.
- **Bounded experiment:** evidence gate passes, net value `3-5`, uncertainty is material, and the test is reversible with a named stop condition.
- **Do not adopt:** evidence gate fails, net value is below `3`, an equivalent already exists, or maintenance exceeds likely benefit.

Recommend at most five adopt-now items. Prefer one smaller mechanism with direct evidence over a broad process package.

## Mechanic-Specific Gates

- **Hooks:** require a deterministic trigger, repeat-safe command, bounded timeout, visible failure, no secret output, and a project trust/reload note.
- **Validation:** require a real project command or deterministic check; never invent one from the stack.
- **Project skills:** require repeated use, a stable trigger, named inputs and output, explicit stop conditions, measurable benefit, and no clean existing owner. Explain why a note, reference, existing-skill update, or validator is insufficient. After human approval, implement separately with `skill-creator`.
- **Skill consolidation:** treat legacy/deprecated text or high word count as inspection signals only. Recommend consolidation or retirement only after current sources and actual usage confirm redundancy.
- **Models/reasoning:** require same-case quality evals. Keep high-risk roles at their current setting without role-specific evidence.
- **Subagents/tasks:** require observable routing triggers and preserved implementation/acceptance separation.
- **New roles/docs:** require repeated responsibility that existing roles or project sources cannot own cleanly.
- **Sync/metadata:** preserve mixed and project-owned files; route file transfer through `mamkin-template-sync`.
- **External tools/providers:** recommendation may describe value, but setup remains a separate human-approved action.

## Success And Rollback

Each adopt-now or experiment item must name:

- Exact files or runtime surface affected.
- Expected benefit and one observable success measure.
- Validation required after adoption.
- Review date or event.
- Rollback or disable path.
- Human decision or trust/restart action, if any.
- Maintenance source and review/retirement trigger.

## Output

Use `docs/process/handoff-packets/project-evolution-audit.md`. Explicitly list useful mechanics that were considered and rejected so future audits do not rediscover them without new evidence.


# SOURCE: docs/process/handoff-packets/project-evolution-audit.md
# Project Evolution Audit Packet

```text
Status: Audit complete | Audit limited | Blocked
Role: project evolution auditor
Project:
Project branch/HEAD:
Project dirty state:
Current Mamkin template/HEAD:
Recorded template commit:
Recorded last sync commit:
Baseline confidence:
Inventory command:
Project maturity evidence:
Project-native evidence inspected:
Existing custom skills/checks:

Adopt now:
  - Mechanic:
    Candidate origin: Template capability | Project-native learning
    Preferred action: Keep source | Update/consolidate existing | Add validator/check | Create project skill | Propose upstream | Merge/retire
    Project evidence:
    Capability state: Missing | Partial | Inactive | Present but misfit | Not applicable
    Benefit score:
    Cost score:
    Net value:
    Why a smaller action is insufficient:
    Exact surfaces:
    Success measure:
    Validation:
    Rollback:
    Maintenance source and review/retirement trigger:
    Human/trust action:

Bounded experiments:
  - Mechanic:
    Evidence and uncertainty:
    Preferred action:
    Net value:
    Experiment and stop condition:
    Success measure:
    Rollback:

Do not adopt:
  - Mechanic:
    Reason:
    Reconsider only if:

Existing project mechanics to preserve:
Project-specific knowledge that must not move upstream:
Upstream proposals (handoff only; no template mutation in this task):
  - Generic problem and anonymized evidence:
    Candidate Mamkin surfaces:
    Success measure and validation:
    Separate Mamkin task required: yes | not applicable
Audit limitations:
Human decisions needed:
Recommended next action:
```


# SOURCE: docs/process/adopt-existing-project.md
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

If the target is dirty, record the original HEAD and exact dirty paths. Do not stash, reset, discard, or silently move them merely to unblock adoption. Ask for the smallest ownership decision. A human may approve preserving one coherent dirty scope on a named branch/commit, or using a separate clean adoption worktree only after proving it will not bypass or overwrite the dirty paths. Then rerun review against the resulting clean pinned target and record the recovery decision in the adoption handoff.

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
4. **Delivery model:** existing local checks, CI coverage, deployment ownership, base branch, feature-branch and integration preference, local commit authority, per-feature external Git approval, cleanup preference, recommended orchestration, occasional parallel work, and genuinely recurring custom roles.

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
- Record project-wide Git delivery defaults in the brief. Do not infer push, PR, merge, or remote-cleanup authority from existing remotes or history.
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
- Git delivery defaults are usable, named feature branches remain the default, and external authority is not implied.
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


# SOURCE: docs/process/handoff-packets/adoption.md
# Adoption Handoff Packet

```text
Status: Review only | Ready for approval | Adoption applied | Adopted with baseline gaps | Blocked | Not eligible - use init | Already initialized - use template sync
Project:
Target repository:
Target branch:
Target HEAD reviewed:
Target HEAD applied:
Target dirty state:
Dirty-target recovery decision:
Mamkin source:
Mamkin source commit:
Upstream verification:
Repository classification:
Existing project sources preserved:
Process files planned or added:
Mixed files requiring or receiving reconciliation:
Existing collisions protected:
Project docs created or adapted:
Project commands discovered:
Git delivery defaults:
Baseline checks run:
Baseline failures or gaps:
MUST involve human gates:
SHOULD involve human gates:
External configuration unchanged:
Mamkin metadata:
Project trust or hook review state:
First coordinator focus:
Recommended orchestration model:
Coordinator transition: fresh task recommended | fresh task approved | same-task and rename explicitly approved | not applicable
Coordinator task id and title:
Starter prompt delivered or manual fallback:
Adoption task final state: waiting for human choice | coordination transferred | same-task coordinator approved | not applicable
Human decisions needed:
Open questions:
Recommended next action:
```


# SOURCE: .agents/skills/mamkin-project-evolution-audit/SKILL.md
---
name: mamkin-project-evolution-audit
description: Audit mature Mamkin projects for evidence-backed, net-positive process evolution. Use after major syncs, recurring workflow friction, or project-native learning that may justify a check, skill update, consolidation, or upstream proposal.
---

# Mamkin Project Evolution Audit

Run a read-only capability and profitability audit. Do not sync or apply changes.

## Workflow

1. Read `AGENTS.md` and `docs/process/project-evolution-audit.md`.
2. Verify project and template repo state. Preserve dirty worktrees.
3. Run the current template's inventory script:

   ```bash
   python3 <template>/scripts/audit_mamkin_evolution.py \
     --project <project> \
     --template <template> \
     --format json
   ```

4. Inspect only evidence needed to judge candidates: current project sources, repeated artifacts, custom mechanics, validation, and bounded history.
5. Apply the protocol's evidence, action-ladder, and net-benefit gates. Absence or a log entry alone is not a recommendation.
6. Render `docs/process/handoff-packets/project-evolution-audit.md` in the response. Do not create a report file.

## Boundaries

- Keep template sync separate: sync transfers files; this skill judges project value.
- A dirty or unverified template may inform the audit, but any proposed sync must wait for a committed, clean, verified source.
- Never edit, install, enable hooks, change models, create external resources, commit, or push during the audit.
- Treat `Propose upstream` as a handoff-only result. Never edit or commit the template repository from a copied-project task.
- Approval of an audit recommendation does not authorize cross-repository implementation. Require a separate human-approved `mamkin-builder` task. Task creation authorizes reassessment only unless its starter scope explicitly authorizes implementation.
- Never create or update a project skill during the audit. Recommend an exact candidate first; after human approval, use `skill-creator` in a separate implementation step.
- Preserve project adaptations and gates.
- Recommend at most five `Adopt now` items. Put reversible uncertainty under `Bounded experiments`; reject low-value novelty.


# SOURCE: .agents/skills/mamkin-adopt/SKILL.md
---
name: mamkin-adopt
description: Adopt Mamkin Builder into an existing project after a verified Mamkin source is available. Use for brownfield repository audits, guarded process-layer seeding, project-context reconstruction, ownership reconciliation, baseline validation, and coordinator handoff. If this project has no Mamkin skills yet, install and use `mamkin-bootstrap` first. Do not use for a new copied template or a project with valid Mamkin metadata.
---

# Mamkin Adopt

Use this skill when an existing repository should gain the Mamkin workflow without replacing its product code, Git history, remotes, deployment state, or project-specific instructions.

## Workflow

1. Read `AGENTS.md` and `docs/process/adopt-existing-project.md`.
2. Classify the repository before editing. Route new copied templates to `mamkin-init` and initialized Mamkin projects to `mamkin-template-sync`.
3. Run the required Git preflight and a read-only inventory. Treat current project sources as authoritative and inspect environment-variable names only.
4. Run the focused brownfield interview only for facts the repository does not establish.
5. Use `scripts/adopt_mamkin_process.py` in review mode to produce the pinned adoption plan.
6. Apply no files until the human approves that exact plan. Re-review when the source commit, target commit, dirty state, or plan digest changes.
7. After approval, seed collision-free process files, reconcile mixed files manually, and create project-owned docs from current evidence rather than template placeholders.
8. Run safe existing checks, complete the adoption self-review, and return `docs/process/handoff-packets/adoption.md`.
9. Follow the protocol's coordinator transition. Do not begin product work in the adoption task unless the human explicitly chooses same-task continuation.

## Boundaries

- Never overwrite an existing target file automatically.
- Never copy product code, tests, migrations, secrets, remotes, provider state, production data, or deployment configuration from the template.
- Do not invent setup, run, validation, architecture, or recovery facts.
- Keep external actions and production changes behind the human gates in `AGENTS.md`.
- Adoption installs process only; it does not implement the upcoming product change.


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
