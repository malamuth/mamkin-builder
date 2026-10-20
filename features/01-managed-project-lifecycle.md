# Managed project lifecycle

Status: local implementation and independent review complete; Merge-ready. The human authorized local fast-forward integration and push to origin/main on 2026-10-20, with the migration plan excluded from published history. Evidence: `docs/follow-ups/managed-project-lifecycle-2026-10-20/`.

## Goal and scope

Add optional portfolio coordination to Mamkin without extending repository write authority. A parent records child coordinators; each child owns its local active-lane ledger. Parent-led rollover requires an exact source baseline and a verified successor receipt. Task retirement and resource cleanup remain separate operations.

Owned scope: reusable process, JSON templates, read-only validators and regression tests, discovery/sync metadata and prompt cases. Project-specific migration plans remain local and are excluded from template delivery. No changes to child repositories, running coordinators, model defaults, providers, live artifacts or existing worktrees.

## Git delivery contract

- Base branch: `main`, `724aeaaf2658e4758daa86c904e8c48983f06c5e`.
- Feature branch: `codex/managed-project-lifecycle`.
- Worktree: current; single implementation writer.
- Delivery mode: feature branch.
- Direct-to-base rationale and approval: N/A.
- Integration path: local fast-forward, authorized after acceptance.
- Merge method: fast-forward.
- Remote and base target: `origin/main`.
- Local Git authority: branch + commit under the authorized local template change.
- External Git authority: full closeout for fast-forward integration and push to `origin/main`; retain branches.
- Remote branch cleanup: retain.
- Closeout owner: coordinator in this chat; retain branch and current checkout after integration.

## Acceptance

- Single-project workflow remains valid without portfolio files; existing active-lane v1 contracts remain compatible.
- Registry identifies one parent, unique child coordinators, exact last-confirmed checkout state and child ledger locations; child count is not the two-track lane cap.
- Transfer records preserve dirty boundaries and all unresolved active/blocked/parked lanes. Successor receipt must match project, task, baseline and lane set before promotion. Failed or unavailable receipt never transfers authority.
- A retired coordinator cannot dispatch; late packets route through the recorded successor. Parent coordination never writes a child repository from the parent task.
- Cleanup distinguishes task completion, accepted integration, chat retirement and worktree removal. Dirty state, uncollected packets, shared/live worktrees and unverified preservation block cleanup. No automatic branch deletion or paid/external action.
- Deterministic CLI tests include malformed input, mismatched receipts, stale registry authority and unsafe cleanup. Independent read-only review checks process and repository boundaries.

## Validation and rollback

Run coordination contract tests, prompt validation, relevant sync/adoption/validation-planner tests and the full standard-library suite before handoff. Exercise the new failure scenarios independently as dry runs; report structural checks separately from model behavior and live rollover.

Before integration rollback is retaining or discarding this isolated branch after preserving review evidence. After integration use a normal revert; project-owned registries and product files are never reset by template sync.

## Result

The final full suite passed 70 tests, including 21 coordination-contract tests; prompt contracts and whitespace checks passed. Independent Critical review returned no blockers after two corrected authority gaps. All six new scenarios passed 36/36 offline rubric points; corrective retests complete offline response coverage for all 50 registered cases. This is not a single passing A/B or fresh isolated execution per case. Actual child migration, model activation, rollover and cleanup remain unperformed and require their own authorization.
