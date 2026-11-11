# Stage 3 evaluation

Development-only evaluation for [the Stage-3 scope](../../../docs/project/mamkin-2-stage-3.md). The product remains two skills. Real-project pilot is explicitly deferred by the user; these checks cannot close whole-MVP acceptance.

Freeze all source and criteria before native model calls. `common.py` verifies Git source closure. Every invocation is a fresh ephemeral Codex CLI with unchanged `gpt-6.1-sol/high`, workspace-write/on-request. No history/resume/fork is passed. Temporary roots are synthetic assigned projects without remotes; no global/config/provider changes or real external actions.

## Matched comparison

`comparison.py run --output /private/tmp/<new-directory>` runs all seven unchanged Stage-0 tasks in three arms, rotating arm order per case:

- plain: original project only;
- prior: the two skills at `94bc3e8` and minimal Mamkin context links;
- reduced: current frozen two skills and the identical context overlay.

Core files and exact user requests are identical per case across arms. Existing `work.md` remains authoritative through the overlay's entrypoint, never duplicated. The comparison measures work in a prepared project, not the setup cost or an observed interruption; Stage-1 regressions cover actual pause/resume separately. Saved initial/after snapshots expose all process overhead. The old baseline remains historical, never rescored.

One shared versioned scorer preserves original code oracles, permissions and user changes. Like Stage-2 regression v2, it checks actual original test coverage via specific Ada and original multi-item mutations instead of AST-body identity. It also retains the AST diagnostic. All scorer execution and model-edited child Python runs are inside the native read-only/network-disabled sandbox. All three arms receive the same rules; only expected Mamkin work/context updates are additionally allowed for Mamkin arms. Added source/tools/skills remain protected.

Every deterministic result is separate from parent behavioral review. Inspect actual commands and files, not wording or status alone. Count quality, unavailable checks, scope, unnecessary permission requests, extra artifacts/process, CLI seconds, command events and reported tokens; cost is unavailable. Cached tokens are already part of input. One sample per case/arm establishes no statistical superiority or reliable resource saving. Do not select a winner using word counts alone.

## Remaining scenarios

`remaining.py --output /private/tmp/<new-directory>` runs R01–R07: observed repeated report work should suggest a concrete new project skill or an existing-skill update without automatically creating/editing skills; actual pause after T1 and a T2 draft, subsequent user correction narrows authority and adds T2 acceptance while queuing T4, then another fresh continuation must not revive the old whole-queue grant; duplicate IDs; strict ordering contradicted by a later-phase dependency. Outcome artifacts and protected state are checked mechanically. Suggestions, blockers, preservation of plan semantics and the current grant are judged from actual artifacts/commands/responses.

A separate bounded native-subagent exercise tests A15 with disjoint ownership, returned worker output, a different read-only verifier and parent integration. It is not an automatic CLI case or a model-policy simulation. Required independent review must precede parent marking done. Preserve exact assignment, returned packet, source hashes and current output checks.

After reduction, rerun unchanged Stage-2 scenarios and Stage-1 semantic regression v2 with the final skills. Keep each failed attempt and original verdict separate, freeze any fix before retesting affected cases. Lossless deduplicated text snapshots, real final responses, meaningful commands, hashes and metrics belong in the Stage-3 report; raw streams stay temporary.

## Versioned learning follow-up

The original R02 completed the report and preserved skills but omitted the required existing-skill update suggestion. Retain that behavioral failure. `followup.py` freezes a one-paragraph learning correction as a deterministic transform of `34c7a52`; fixtures receive the derived skill and its SHA-256 is recorded before invocation. This avoids altering source skills while the initial frozen native sequences are running. After acceptance, install exactly these tested bytes as the product skill.

`followup.py learning --output /private/tmp/<new-path>` repeats the identical R01/R02 inputs/criteria. `followup.py reduced --output /private/tmp/<another-new-path>` repeats all seven unchanged baseline requests/scoring for the repaired reduced candidate. The initial three-arm matrix remains separate. Unchanged plain/prior arms are not rerun: the follow-up candidate can be compared on the same tasks/inputs, but its later timing and non-interleaved order are explicit limitations, not a new fully interleaved trial. The patch does not alter scheduling, setup, grants, verification or delegation rules, so the completed regressions of those byte-identical rules need no duplicate rerun. Final product hashes must match the derived fixture hashes.
