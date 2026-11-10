# Mamkin 2.0 Stage 0 baseline

This directory freezes seven executable synthetic-project cases before any baseline model run. It is evaluation material, not a product CLI or a Mamkin 2.0 implementation.

Suite version 2 corrects an over-restrictive version 1 preservation rule: authorized code fixes may add regression tests while preserving the original test bodies. One B01 smoke run against version 1 exposed the mistake; it is retained as a methodology check and is not rescored or counted in the version 2 baseline. All version 2 cases start from fresh inputs after the corrected suite commit.

The requirements and project status live in [the MVP plan](../../../docs/project/mamkin-2-mvp-plan.md). The baseline uses ordinary Codex with the same project inputs intended for the later candidate comparison. No Mamkin 1.x/2.0 project instructions, skill, role card, handoff template or evaluation oracle is copied into the model's working directory.

## Frozen inputs

- `cases.json`: exact prompts, project overlays, allowed changes and behavioral criteria.
- `suite.py`: shared fixture files, preparation, independent code oracles and preservation checks.
- Model: `gpt-6.1-sol`; reasoning effort: `high`; one fresh run per case.
- Runtime checked before preparation: `codex-cli 0.167.0-alpha.3.2`.
- Model sandbox: `workspace-write`, with normal approvals and existing execution rules. No bypass flags, global configuration edits, credential copying, dependency installation or external project writes.
- Each fixture is a synthetic disposable Git repository outside the Mamkin checkout. It has no remote. It is an assigned evaluation copy, not another real project.
- Fixture `AGENTS.md` contains only project commands and preservation/external-action boundaries. Existing user-level Codex guidance may still apply; its presence is a comparison condition, not evidence of a fully empty system prompt.

Keep the exact CLI version, model, effort, user-level guidance/tool environment and sandbox comparable between arms. If any changes, record it and rerun a matched baseline instead of presenting old and new outputs as a controlled comparison.

## Coverage and limits

| Case | Work | Acceptance scenarios |
| --- | --- | --- |
| B01 | Empty-cart bugfix with dirty user code and note | A01, A11 |
| B02 | Materially missing discount policy | A02 |
| B03 | Resume a prepared partial-work snapshot | A03, snapshot only |
| B04 | Stale done record contradicted by current code | A04, A18 |
| B05 | Select one available backlog task | A05, A08 |
| B06 | Strict stage and external-action boundary | A06, A09 |
| B07 | Required owner check unavailable | A12 |

These fixtures test actual source edits, preservation and operational responses. B03 is a prepared interrupted-state snapshot, not an observed real interruption or a complete multi-session workflow. The suite does not establish setup, all hybrid modes, genuine long-context recovery, real-project usefulness or broad reliability. Those remain Stage 1–3 checks under the product plan. One sample per case does not establish repeatability or statistical significance.

## Reproduction

Run oracle controls before any model run:

```sh
python3 -B evals/mamkin-2/stage-0/suite.py preflight
```

For each case, materialize a fresh absolute path under a new evaluation directory, for example `/private/tmp/mamkin-2-stage-0-run/B01`. Never reuse an evaluated directory as a fresh input. Preparation refuses an existing target.

```sh
python3 -B evals/mamkin-2/stage-0/suite.py prepare --case B01 --root /private/tmp/mamkin-2-stage-0-run/B01
```

Preparation records input file hashes, dirty state, base commit and exact prompt/suite/cases hashes in the sibling `B01-input.json`, outside the agent's project. Commit the frozen suite before executing model cases; record that commit in the run evidence.

Use an argv-based launcher to pass `suite.py prompt --case B01` as stdin to this command, collecting stdout/stderr and the final message outside the fixture:

```text
codex --no-daemon -a on-request exec --ephemeral --json
  --model gpt-6.1-sol -c model_reasoning_effort="high"
  --sandbox workspace-write --skip-git-repo-check
  --cd /private/tmp/mamkin-2-stage-0-run/B01
  --output-last-message <outside-fixture>/B01-final.txt -
```

The Codex CLI uses its existing account authentication internally. Do not read, copy or print credential material. If startup needs a login, provider setup, paid-service decision or weakened restrictions, preserve preparation and report the exact missing human action. A startup failure is not an evaluated case or a baseline result. Ordinary sandbox restrictions may prevent CLI runtime-state or network access; do not disguise that as model failure.

After a completed run, invoke:

```sh
python3 -B evals/mamkin-2/stage-0/suite.py check --case B01 --root /private/tmp/mamkin-2-stage-0-run/B01
```

Do not change prompts, initial files, or acceptance after seeing outputs. A correction creates a new suite version and invalidates affected unmatched comparisons. Model-created tests cannot replace the independent oracle.

## Scoring and retained evidence

Deterministic results cover code behavior, existing tests, protected files and known user edits. The parent separately inspects final responses and tool evidence against the frozen behavioral criteria. Automated preservation passes alone never establish behavioral success; no keyword matcher issues an overall pass.

Keep each case's final response, actual patch or output snapshot, input hashes, deterministic result, behavioral verdict and concise supporting observations. Record unexpected/new files, unnecessary approvals, and external-action attempts. Retain only task-relevant command evidence; review evidence for private data before adding it to Git.

Record elapsed run time, command/tool-event counts and reported token usage when the CLI exposes them. These are observed metrics, not inferred savings. Cost remains unavailable unless the runtime explicitly reports it. A timed-out or failed run retains that status; do not fill missing metrics with zero.

Full raw event streams stay temporary unless needed to explain a verdict or recover a result. Candidate comparison must preserve the same scoring and also inspect task quality, continuation, user interventions and unnecessary process.
