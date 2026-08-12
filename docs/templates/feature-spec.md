# Feature NN: Title

## Product Value

Explain the concrete value this feature creates.

## User Or Owner Story

As a ...

I want ...

So that ...

## Scope

- In scope:
- Also in scope:

## Out Of Scope

- Not in this feature:
- Deferred:

## Dependencies

- Prior features:
- External services:
- Human setup:

## Git Delivery Contract

- Base branch:
- Feature branch: `codex/fNN-short-scope`
- Worktree: current | separate
- Delivery mode: feature branch | direct-to-base exception
- Direct-to-base rationale and approval: N/A | exact decision
- Integration path: pull request | local
- Merge method: merge commit | squash | fast-forward
- Remote and base target: `<remote>/<base branch>`
- Local Git authority: branch + commit | working tree only
- External Git authority: none | push branch + open PR | full closeout
- Remote branch cleanup: retain | delete after verified integration
- Closeout owner: coordinator

## Parallel Safety

- May run in parallel with:
- Must not run in parallel with:
- Expected files or surfaces:
- Shared schemas, migrations, APIs, lockfiles, generated sources, configuration, fixtures, or environments:
- Cross-track assumptions:
- Combined checks required after integration:

## Design And Architecture Notes

Describe the relevant data model, API, UI, worker, storage, or integration choices. Keep this specific enough for implementation, but avoid over-designing future features.

## Human-In-The-Loop Gates

MUST involve human:

- TBD

SHOULD involve human:

- TBD

Agent may decide:

- TBD

## Acceptance Criteria

- The feature does ...
- The feature rejects or handles ...
- The relevant state is visible or verifiable ...
- Failure cases are covered ...

## Verification Scenarios

- Happy path and expected observable outcome:
- Boundary or error case and expected observable outcome:
- State, data, or cleanup behavior that must be verified:

## Automated Test Plan

- Unit tests:
- Integration/API tests:
- UI/E2E tests:
- Migration or data tests:

## Walkthrough Requirements

- Required environment:
- Required accounts or services:
- Human actions needed:
- Evidence to capture:
- Detailed commands and steps belong in `docs/walkthroughs/`, not this spec.

## Implementation Notes

- Suggested files or modules:
- Existing patterns to follow:
- Generated artifacts to watch:

## Implementation Readiness Check

This feature is ready for implementation when:

- Scope is bounded.
- Acceptance criteria are testable.
- Human gates are explicit.
- Required dependencies are available or called out.
- Git delivery, authority, and closeout ownership are explicit; direct-to-base has a human-approved rationale.
- Parallel safety is explicit when another track may run at the same time.
- Verification scenarios and evidence needs are clear enough for the coordinator to create or assign a runbook.
