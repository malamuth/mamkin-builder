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
