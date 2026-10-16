# Sol coordinator bounded execution A/B — 2026-10-16

Both models solved the real bounded code task and passed independent acceptance. A blind reviewer gave both 6/6 quality dimensions and preferred arm b's broader retained regression coverage. This is a task-specific implementation result, not a general model ranking or a measured cost/speed improvement.

| Arm | Requested model / effort | Independent acceptance | Quality rubric | Blocking findings |
| --- | --- | ---: | ---: | ---: |
| a | `gpt-5.6-sol` / `high` | 18/18 | 6/6 | 0 |
| b | `gpt-6.1-sol` / `high` | 18/18 | 6/6 | 0 |

## Actual task and locked criteria

The source is Mamkin's current `scripts/validate_coordination_contracts.py` and its tests at `bb590c770e6ecedc74dca3d4faa0c7267b231495`; no defect was planted. Array/object-valued lane statuses cause an uncaught `TypeError`, and JSON boolean `true` or float `1.0` is accepted as schema version 1. Invalid UTF-8 was initially suspected but reproduction showed it already receives a normal diagnostic; it stayed a preservation control.

`task.md` and `acceptance.py` were committed before either implementation at `9a1802b7e6c598a7087a1d2962171012461088a1`. Their SHA-256 digests are recorded in `parent-validation.json`. The original five unit tests passed. The fixed independent acceptance suite ran 18 test methods and exposed eight failing assertions and two error subtests on the original implementation. Its loops also exercise declared type/value combinations and preservation controls.

## Execution isolation and evidence

- Two fresh subagents, `/root/execution_arm_56` and `/root/execution_arm_61`, received the same prompt and snapshot bytes; only the assigned root path and launch model differed.
- Both arms used the repaired Mamkin policy, fixed high effort, the same tools and permissions, and exclusive ownership of two files in separate evaluation directories. They were prohibited from reading each other's work, prior scores, or the independent acceptance code.
- These were copies inside the parent's ignored `tmp/sol-ab-F1Mk33wp/`, not new product repositories, independent Git worktrees, or sidebar tasks. The unrelated note is an explicit evaluation fixture, not private user data or a genuine dirty-Git exercise.
- The parent reran each arm's retained tests (a: 10 methods, b: 9) and executed the same locked acceptance suite (18/18 for each). File hash comparison confirmed only the two assigned files changed, including byte preservation of the protected note and all policies.
- A fresh `gpt-6-astra` / `high` reviewer statically reviewed the anonymized code, tests, handoffs, and parent-executed evidence. The model mapping was not supplied. The reviewer did not repeat passing suites or implement either result.

The 5.6 implementation adds a shared schema-version helper; the 6.1 implementation performs exact integer checks inline. Both guard the status type before set membership. Both satisfy the defined behavior and avoid executing the declared consumer command. The reviewer's modest preference for 6.1 concerns retained test coverage; neither variant needs corrective work to pass this task.

## Retained artifacts and reproduction

`arm-prompt.txt` is the shared dispatch text with `{ARM_ROOT}` replaced by `tmp/sol-ab-F1Mk33wp/a` or `b` under the repository. The arm handoff JSON files preserve the returned implementation packets. `review-scores.json` preserves the complete blind review. `parent-validation.json` records independent results, provenance, and hashes.

`arm-a.patch` and `arm-b.patch` contain complete source/test differences against the named source commit. They use zero-context hunks so patch context whitespace does not pollute the repository's whitespace checks. In a disposable copy of the source snapshot, apply the chosen patch with `git apply --unidiff-zero`, then run `python3 -B -m unittest tests.test_validate_coordination_contracts` there and `python3 -B <evidence-directory>/acceptance.py --root <copy>`. The original evaluation copies are retained under the ignored temporary path for inspection; the committed source reference and patches support later reproduction if that path is removed.

## Decision boundary

This run supports using 6.1 Sol/high for this reversible, fully specified implementation responsibility. Together with the twelve-case policy retest it removes the earlier lack of any executed code-task evidence. It does not exercise a live coordinator's human steering, actual delegation/retest cycle, Figma or deployment tools, or long-context state management.

The active default and the main template validator are unchanged: the user requested comparison, and the two implementations remain evaluated artifacts. No push, merge, installation, external mutation, or model-setting change was part of the experiment.

Tokens, total tool calls, model latency, and cost were unavailable. Unit-test runtime and parent receipt order are not valid substitutes for model efficiency. The implementation samples and judge were run once; repeatability and workload breadth remain unmeasured.
