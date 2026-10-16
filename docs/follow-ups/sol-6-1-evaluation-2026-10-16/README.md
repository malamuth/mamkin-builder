# Sol 6.1 Coordinator A/B — 2026-10-16

## Result

The matched policy-response comparison does not authorize a model switch.

| Arm | Model / effort | Passed cases | Rubric points |
| --- | --- | ---: | ---: |
| A | `gpt-6.1-sol` / `high` | 9/12 | 69/72 |
| B | `gpt-5.6-sol` / `high` | 2/12 | 61/72 |

The blind scorer preferred Arm A, but the hard gate requires every case and every dimension to pass. Keep `gpt-5.6-sol` / `high` active until a matched rerun passes; this is conservative migration policy, not a claim that the baseline performed better.

## Protocol

- Repository snapshot: `af39365f7960c855cdb0521e50a5c3927a0ed96b` on `codex/sol-6-1-process-simplification`.
- One fresh read-only subagent per arm, identical prompt and twelve cases, model hidden from the response.
- Arms read the same seven current policy files and were prohibited from opening expected outputs or prior evaluation history.
- One independent `gpt-6-astra` / `high` scorer received anonymized arms A and B, then applied the six binary dimensions from `docs/process/prompt-evals.md`.
- No repository or external mutation occurred in either arm.

Raw policy responses are in `arm-a-gpt-6.1-sol-high.json` and `arm-b-gpt-5.6-sol-high.json`. Case-level scoring and the blind comparison are in `scores.json`.

## Failures

Both arms missed:

- `read-only-audit`: explicitly verify and report unchanged Git status;
- `external-action-gate`: include material consequences in the approval request;
- `post-reset-rollover`: prepare a committed reset baseline.

The baseline arm additionally omitted required handoff or evidence details in bounded change, dirty-worktree, pull-based handoff, cross-repository correction, external micro-slice receipt, Deep diagnosis, and Git delivery cases.

## Evidence Boundary

This is one run per model over batched policy simulations. It does not measure executed implementation quality, repeated-run variance, live steering, actual external tools, tokens, cost, or per-arm latency. Tool-call and resource telemetry were unavailable; concurrent wall time is not comparable per arm.

Next evaluation should keep the same models and effort, repair or clarify one common instruction group, and rerun the same fixed cases. Do not combine that prompt ablation with a move to `medium` effort.
