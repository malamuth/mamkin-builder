# Agent Orchestration

This is the coordinator manual after init. Workers do not read it by default; they receive `AGENTS.md`, one role card, the relevant feature or walkthrough, and one return packet.

## Scope And Conditional Reading

Keep live project state in `docs/project/`, `features/`, `docs/walkthroughs/`, and `docs/follow-ups/`. Edit this manual only for reusable coordination policy.

The coordinator reads:

- This manual plus the current brief, decision log, roadmap, and relevant feature material.
- `docs/process/execution-lane-routing.md` only before delegation, subagent use, or two-track admission.
- `docs/process/git-delivery.md` when activating a write-capable feature, assigning its implementation lane, or closing it out.
- `docs/process/thread-operations.md` only when creating, receiving from, or recovering a separate task.
- `docs/process/naming-conventions.md` only when naming or renaming a durable task or follow-up document.
- The one packet file needed for the current handoff. Use `docs/process/handoff-packets.md` only when the correct packet is unclear.
- `docs/process/context-health-audit.md` only when context drift or source confusion is suspected.

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

Built-in role cards live under `docs/process/roles/`; matching launch presets live under `.codex/agents/`.

Use `gpt-5.6-terra` at medium effort for bounded implementation, deployment, and read-only subagents when runtime overrides are available. Keep architect, reviewer, walkthrough, design, UX, or otherwise ambiguous/high-risk work at its preset default until role-specific execution evals support a lower setting.

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
