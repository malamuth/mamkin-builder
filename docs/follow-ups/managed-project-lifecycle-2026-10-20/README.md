# Managed-project lifecycle verification

Scope: optional portfolio registry, child lane ownership, verified coordinator transfer and separate chat/worktree cleanup. Implementation base: `724aeaaf2658e4758daa86c904e8c48983f06c5e`; feature branch: `codex/managed-project-lifecycle`. No model default changed in this feature.

## Executed local evidence

- Final full standard-library suite: **70 tests passed**. The coordination module contains **21 tests**, including function/CLI negatives for inconsistent transfer states, lost lanes, wrong successor identity/checkout/hash, dirty preservation, unsafe cleanup and malformed JSON.
- Prompt contract validator: passed; **50 registered cases**. This is a structural check, not 50 executed behavioral workflows.
- `git diff --check`: passed. Change-aware planner selects coordination, prompt, evolution, sync and planner checks; the full suite includes their test modules.
- Independent Critical review: two initial P2 contract findings corrected and retested; **No blocking findings**. See `review.md`.
- `candidate-source-sha256.json` records the corrected core source bytes. Final Git handoff supplies the containing commit; no self-referential future commit id is embedded here.

## Offline instruction-response experiment

Two fresh bounded agents received all 50 case requests/setups without expected objects. The baseline arm read policy at the base commit; the candidate read the initial working tree. The assignment imposed a 1–3 sentence response limit. Each returned hypothetical next actions; neither performed the case operations. A separate Deep scorer read the expected objects and applied all six rubric dimensions.

The grouped run **did not pass the full quality gate**: baseline **26/50 cases, 275/300 points**; candidate with the first six-case retest **30/50 cases, 279/300 points**. Preserve these results in `grouped-scoring.json`. Do not present the numerical difference as causal improvement: responses were grouped, constrained, generated once per arm, and the candidate score combines outputs from different stages. The scorer identified missing operational steps in responses; these omissions alone do not prove source-policy defects. Initial candidate sources were not committed; the corrected source manifest does not retroactively identify that initial tree.

Review independently found and corrected two actual source gaps. A later explicit preparation paragraph requires a complete child assignment before requesting missing dispatch authority. Complete, uncapped responses for all six new managed cases then passed independent Critical scoring: **6/6 cases, 36/36 points**, with no source blockers. See `managed-final-responses.json` and `managed-final-scoring.json`. The earlier failed outputs remain unchanged.

The 18 other candidate cases with missing steps were rerun without the artificial sentence cap, reading the applicable current policy and referenced task fixtures. The independent Deep scorer passed **18/18 cases, 108/108 points**, without requiring another source-policy change. See `coverage-retest-responses.json` and `coverage-retest-scoring.json`. Combining the 26 already-passing non-managed cases, 18 corrective responses and six complete managed responses gives final **offline coverage of all 50 cases**, not one all-passing paired run. This is corrective coverage, not a repeat of the original paired experiment with identical prompts.

## Reproduction and limits

Run `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests` and `python3 scripts/validate_prompt_contracts.py` from the feature source. For instruction responses, use `evals/mamkin-prompt-cases.json`, expose request/setup and applicable policy to the responding agent, keep expected objects for a separate scorer, and use the six-dimension rubric in `docs/process/prompt-evals.md`. Avoid sentence limits that remove operational fields.

The response tests were grouped rather than fresh isolated execution per case. No real coordination workflow, migration, task creation/send, authentic successor receipt, archive, worktree deletion, paid run, provider or remote operation was exercised by these tests. Effective inherited response model, latency, tokens and cost were unavailable. The named Astra profiles identify assigned reviewers/scorers, not verified runtime identity of generation arms. No Sol 6.1 reliability, efficiency, repeated-run or full live-rollout result follows. Fresh per-case execution and an explicitly authorized operational pilot remain outside this local acceptance.
