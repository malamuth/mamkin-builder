# Sol 6.1 coordinator A/B retest — 2026-10-16

The requested three-instruction repair is complete. Both models now pass the audit-status, external-approval consequences, and committed-reset-baseline cases in the independent blind scoring.

| Model / effort | Initial policy run | Retest | Retest rubric points |
| --- | ---: | ---: | ---: |
| `gpt-5.6-sol` / `high` | 2/12 | 9/12 | 69/72 |
| `gpt-6.1-sol` / `high` | 9/12 | 12/12 | 72/72 |

The candidate passes this twelve-case policy-simulation gate. The active runtime was not changed by the repair-and-retest request. Executed coordination, repeated-run reliability, resource efficiency, and reduced effort remain untested.

## Controlled change

Instruction snapshot: `fbe34980168fa67a130734647d02e89bc05318d9`. Compared with the first run's snapshot, the only policy changes are:

- `docs/process/agent-orchestration.md`: compare initial/final Git status and report unchanged state for a read-only repository audit.
- The same manual: name the exact external action/target and explain relevant cost, visibility, data effects, or recovery limits in approval requests.
- `docs/process/context-health-audit.md`: name failed-reset evidence and require a committed source-grounded baseline before starting the next coordinator. The read-only audit recommends that preparation rather than writing the baseline itself.

The case file and six-dimension rubric were unchanged. The common arm prompt is identical to the first run except for the snapshot commit. No targeted hints or prior scores were supplied to either arm.

## Execution and artifacts

- Fresh read-only arms: `/root/ab_retest_56` and `/root/ab_retest_61`, requested at `high` with their exact model overrides; neither received parent conversation history.
- Both read the same seven policy sources listed in `arm-prompt.txt`. Expected answers and evaluation history were excluded.
- Fresh scorer: `/root/ab_retest_blind_scorer`, requested as `gpt-6-astra` / `high`, with anonymous A/B outputs and the same scorer instructions and expected objects as the first run.
- Arm A is 5.6 Sol; Arm B is 6.1 Sol. This reverses the first run's anonymized order. Models were not disclosed in the scorer's arm inputs.
- Both arms completed before evidence files were written. Git status after their completion was clean at the instruction snapshot.

`arm-prompt.txt` preserves the exact common dispatch text. The two arm JSON files preserve their returned JSON. `scorer-instructions.txt` preserves the scoring instruction prefix; the dispatched scorer prompt appended `Arm A responses:` and `Arm B responses:` followed by those two JSON objects in that order. `scores.json` preserves the complete returned scorer output, including every dimension and reason.

## Remaining baseline omissions

The scorer failed 5.6 Sol on three details: reporting the dirty boundary when work proceeds safely, naming the coordinator in the final packet, and explicitly recording unknown-root-cause/conflicting-source risk signals. It reported no unnecessary approval requests in either arm.

## Limits and interpretation

These are one fresh sample per model and one fresh judge sample per evaluation round. The before/after gains cannot be attributed entirely to the instruction repair. Response variability and judge variability are not measured.

There is a visible interpretation difference between judges: the first round required an explicit smallest compatibility-correction path and a bounded external-change receipt, while this round accepted owner-led correction and rollback/visual evidence. Historical scores are preserved and have not been rescored or relaxed. The raw twelve-of-twelve score should be read with that grading limitation.

Tokens, cost, tool-call totals, and comparable per-arm latency were unavailable. No product code, external system, real delegation cycle, or interactive walkthrough was exercised. A representative executed coordinator task is the next useful check before broad default adoption; the evidence does not support lowering effort.
