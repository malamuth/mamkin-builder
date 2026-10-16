# Sol 6.1 coordinator activation and accepted validator integration

Decision date: 2026-10-16. Starting state: `b311eb2ccf3834533233de0ec938552c9e5b94e4` on `codex/sol-6-1-process-simplification`, with a clean worktree.

The human explicitly requested applying the Sol 6.1 implementation and switching the coordinator default to `gpt-6.1-sol` / `high`. This changes the template's project-local default, not user-level configuration or already-running tasks. The existing delivery contract continues: local branch and commits, retain the branch, no push or base integration assigned.

## Applied variant

Apply exactly `docs/follow-ups/sol-6-1-execution-2026-10-16/arm-b.patch` to the main template's validator and tests. Expected Git blob IDs from the accepted variant:

- `scripts/validate_coordination_contracts.py`: `b19c29ad0f8a22371d4f7aeed55896c60501b96b`.
- `tests/test_validate_coordination_contracts.py`: `1cded3354dcfbb6ce4d1940bbb6ed2c8e04a82e8`.

The code requires the exact JSON integer 1 for schema versions and validates the lane status type before set membership. Tests cover function and CLI behavior, input preservation, existing error handling, valid statuses, and consumer-command non-execution. This is the variant already reviewed independently with no blocking findings; optional review suggestions are not folded into this integration.

## Model decision and evidence

Activate coordinator `gpt-6.1-sol` / `high` in `.codex/config.toml`, current model policy, and routing documentation. Retain all Economy/Balanced Terra and Deep/Critical Astra settings. Preserve historical experiment decisions and scores.

Evidence: the matched policy retest scored 12/12 and 72/72 for Sol 6.1/high. The real bounded implementation scored 18/18 independent acceptance methods and 6/6 quality dimensions; both models passed. The reviewer modestly preferred Sol 6.1's retained tests. Full evidence remains in `sol-6-1-retest-2026-10-16/` and `sol-6-1-execution-2026-10-16/` beside this record.

This is an explicit adoption decision with bounded evidence, not proof of general superiority or improved cost/latency. Long coordinator workflows, repeated-run reliability, and medium effort remain outside the tested scope. Reverting the project-local model to the recorded previous `gpt-5.6-sol` / `high` is the scoped fallback if project evidence justifies it; do not silently alter specialist risk floors.

## Verification

Both integrated source blob IDs match the accepted variant exactly. The 9-test regression suite and the unchanged 18-method independent acceptance suite passed against the main repository. Change-aware validation also passed all 8 model-routing tests, prompt contracts, and whitespace checks. Only the coordinator model and its explanatory comment changed in runtime configuration; effort remains high and current-policy metadata agrees. Historical A/B artifacts and specialist settings were preserved.
