# Astra Evaluation — 2026-09-08

## Decision

The coordinator gate is incomplete. Restore explicit Sol/medium there; keep Astra/high and Astra/xhigh as user-directed specialist pilots. Astra outscored Sol in this sample, but the six-dimension gate does not average failures away. This is not proof that Sol is superior or a broad Astra rejection.

| Evaluation | Sol | Astra | Proof boundary |
| --- | --- | --- | --- |
| 36 batched policy responses, medium | 22/36 strict passes | 31/36 strict passes | Hypothetical intended actions only; independent blinded grading |
| Bounded implementation, medium | 6/6 rubric | 6/6 rubric | Three assigned tests and five independent checks each |
| Read-only diagnosis, high | 5/6 rubric | 6/6 rubric | Correct defect in both; Sol chose an incorrect Balanced floor |
| Critical review, xhigh | 6/6 rubric | 6/6 rubric | Three synthetic defects found, no real release acceptance |

One of Astra's five strict policy failures is source/oracle ambiguity. Its answer limits manual adoption reconciliation to approved ownership, which the actual adoption protocol permits; the oracle blanket prohibition is stricter. Preserve the raw grader score and this adjudication. The other four omissions concern formatter rejection, implementation-approval boundary, worker escalation conditions, and environment-variable-name inventory. These are policy-response omissions, not observed unsafe external actions.

## Method And Evidence

`manifest.json` records dispatched models/efforts, source commit, prompt hash, replication count, label mapping, and limitations. `policy.md` is the identical process snapshot supplied to all participants. `policy-inputs.json` omits expected answers; `oracle.json` was held out. Two stale active Sol model names were corrected in the oracle before dispatch. All other historical evidence remains intact.

Six fresh subagents ran matched prompts differing only in arm paths and model; medium arms performed all 36 scenarios and an isolated implementation. High and xhigh arms performed local reproductions. The current prompt snapshot was fixed across models; historical versus new prompt ablation was not performed. Common host/evaluation instructions also influenced behavior. Independent graders did not implement the fixtures. Coordinator policy labels were blinded (X=Astra, Y=Sol) until scoring; the other graders knew the arms. Source-aware adjudication is explicitly retained rather than silently changing scores.

Each arm directory contains original sources, its unmodified raw `output.json`, and the final implementation where applicable. `initial-hashes.json` proves identical initial fixtures and supports preservation checks. `acceptance-results.json` is the parent's independently executed five-case-per-arm implementation check, including Unicode, order, empty inputs, and nonmutation. `diagnosis-scores.json`, `implementation-scores.json`, `critical-scores.json`, and `policy-scores.json` contain independent per-dimension grading and limits. Reproduction execution is recorded by the participants; graders inspected records and source hashes rather than witnessing every tool call. Raw paths refer to the original ignored local fixture directory; this archive retains the referenced contents for review.

## Reproduce The Deterministic Acceptance

Run from the repository root:

```bash
python3 -B docs/follow-ups/astra-evaluation-2026-09-08/acceptance.py
```

The script writes `acceptance-results.json` beside itself. It checks the archived final implementations and all initial fixture hashes. Original defective implementation bytes remain in the high/xhigh arm directories. Re-running model trials requires fresh arm copies, the same task briefs and policy inputs, exact model/effort dispatch, and independent grading; merely re-running Python does not repeat the model evaluation.

## Limits And Next Experiment

One trial per arm; 36 scenarios share one context per model. The 110-word response cap and supplied policy subset may contribute to omissions. Tasks were synthetic and explicitly constrained against external actions; they do not independently establish safety under a real runtime. No actual delegation, live user steering, UI/Figma action, real adoption/sync, production migration, or Sambl task was executed. Cost, tokens, comparable tool counts and latency are unavailable; self-reported observation boundaries differ. Actual model introspection is unavailable beyond the accepted dispatch configuration.

Next: resolve the adoption oracle ambiguity in a separate scoped test change, then run focused full-packet coordinator cases with the relevant task-specific protocols supplied and no artificial 110-word cap. Follow with a realistic Sambl read-only review and bounded component-document task in a separately approved Sambl task, preserving its current high effort. Do not lower coordinator effort during that model comparison. The template source still requires Git closeout or explicit local-only source approval before downstream apply.
