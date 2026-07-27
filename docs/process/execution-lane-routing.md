# Execution Lane Routing

Use this file to choose between a same-task subagent and a separate Codex task, and to admit at most two independent work tracks. A Codex task and thread are the same durable, user-visible lane in this process.

## Core Boundary

- A separate task owns an independent workstream.
- A subagent performs bounded delegation inside its parent task.
- Prefer a subagent when every subagent condition below passes. Use a separate task when any separate-task trigger applies.
- The parent task remains accountable for subagent scope, evidence, edits, and validation.
- One subagent must not both implement a change and provide its acceptance verdict.

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
- Write ownership spans multiple components or affects a shared API, schema, migration, auth/security boundary, lockfile, generated source, global configuration, or external integration.
- The work cannot be bounded to one prompt with explicit allowed files, observable success criteria, and a known validation path.
- Verification needs manual judgment, interactive UI, accounts, secrets, external systems, environment setup, or a defect/retest cycle.
- The result needs a durable handoff packet, user-visible progress, or clean context isolated from the coordinator.
- Source ownership overlaps another active writer or cannot be proved disjoint.

Architecture, implementation, walkthrough, deployment, or specialist work uses a separate task only when one of these triggers applies. A bounded pass in any role may be a subagent when every subagent condition passes and acceptance remains independently owned.

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
