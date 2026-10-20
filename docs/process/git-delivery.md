# Git Delivery

Use this protocol for every write-capable feature or substantive slice. It owns the path from accepted planning baseline to clean integrated repository state. Project commands and external-action gates still come from `AGENTS.md`.

## Micro-Slice Contract

Avoid a feature spec, durable task, dedicated branch, or walkthrough lane when every condition is true:

- one reversible surface and one owner;
- no cross-component behavior, shared contract/schema/migration, dependency, generated source, security/data/deployment boundary, or product-code change;
- no concurrent writer or cross-repository consumption;
- one focused deterministic check or bounded external-artifact inspection decides success;
- rollback is explicit, external mutation separately authorized, and current status records scope, state, owner, check, evidence, and stop boundary.

Product code still uses a feature branch. Process/admin-only edits may use an approved direct-to-base exception; external-artifact-only work may use its approved project branch. External artifacts, public behavior, manual/nondeterministic judgment, and defect/retest cycles keep independent acceptance. Otherwise the parent may run the focused check and retain one receipt. Promote to the normal contract before further writes if any criterion fails.

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

Use `feature branch` by default, named `codex/fNN-short-scope`, from a clean accepted baseline. A separate writer normally owns a worktree; one same-task lane may use the current worktree without overlap.

`direct-to-base exception` is allowed only when all are true:

- the change is a small administrative or process-only edit, not feature behavior;
- it changes no shared API, schema, migration, dependency/lockfile, generated source, security boundary, or production configuration;
- no other writer is active and the base is clean;
- the human explicitly approves the exception.

Urgent work still uses a branch unless the human approves a named exception.

## Existing Dirty-Base Recovery

If feature writes predate the contract, stop and inventory the dirty state. Do not stash, reset, discard, or silently move a mixed worktree.

- If every dirty path belongs to one human-confirmed feature, create its branch while preserving the worktree, then commit and validate there.
- If unrelated work or features are mixed, present path ownership and recovery first. Separate only with clear provenance; otherwise ask for the smallest decision.
- Record the original base and dirty boundary. Recovery grants no external authority or acceptance.

## Authority

Local branching and commits may proceed under `branch + commit`; runtime approval may still be required. Workers never infer push, PR, merge, or remote-delete authority.

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

Managed chat/worktree cleanup also requires the dependency and preservation preflight in `docs/process/managed-projects.md`.

- `Ready for walkthrough`: committed implementation awaits independent acceptance.
- `Merge-ready`: accepted commit is ready to integrate; Git closeout is incomplete.
- `Ready for Git closeout`: acceptance passed but required integration authority is missing.
- `Delivered`: accepted changes are integrated, required remote updates are verified, cleanup matches the contract, and the base state is clean.
- `Blocked`: state, authority, conflict, validation, or ownership prevents safe progress.

Rollback before integration is branch/worktree removal after preserving any requested evidence. After integration, use a normal revert or project-approved recovery path; never rewrite shared history unless the human explicitly approves the exact destructive action.
