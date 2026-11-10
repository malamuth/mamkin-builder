# Mamkin 2.0 Stage 1 checks

The frozen cases cover setup, repeated setup, actual partial work, a fresh chat continuing that work, unknown commands, and an unavailable mandatory acceptance check. Requirements and delivery boundary: [Stage 1](../../../docs/project/mamkin-2-stage-1.md).

`cases.json` fixes eight prompts and behavioral criteria before model execution. `checks.py` prepares synthetic projects using the frozen Stage-0 cart input, installs only the two new `SKILL.md` files, and checks code behavior and preservation. It is evaluation code, not a product runtime. Do not expose the oracle or previous conclusions to the evaluated agent.

Each prompt is sent to a new `codex exec --ephemeral` with the same installed CLI, requested `gpt-6.1-sol/high`, `workspace-write`, normal approvals and retained user rules used in Stage 0. No `resume`, `fork`, prior response or copied conversation is supplied. Record thread identity hashes when exposed to verify independent sessions. Runtime launcher permission may be needed for native initialization; model sandbox restrictions remain unchanged.

Parent code oracles and model-edited tests run through `codex sandbox` with read-only filesystem policy and network disabled, rather than inheriting an elevated launcher's write access. A stopped or incomplete sequence exits nonzero after retaining its case evidence. Preservation checks allow insertion of new links among original instruction lines.

S01–S04 share the actual evolving `cycle` files. S03 is explicitly stopped after writing and checking a helper; S04 receives only its short continuation prompt and the current project files. This tests a deliberate saved pause and a fresh chat, not recovery from an unannounced crash. S05 uses a separate empty project. Before S06 the evaluator adds `release.md` with a missing mandatory owner check; the prompt explicitly introduces the newer acceptance condition.

S07 adds a previously authorized queued adjacent task while the current task remains blocked. S08 supplies the real owner-check executable. Both receive the same short continuation prompt; the agent must reconcile the current blocker, then resume only that task when the missing check arrives. These checks were added following static review before any behavioral run.

Save each input snapshot/hash, output patch, changed files, final response, command evidence, runtime result, reported usage and separate parent verdict. Capture working state before the next invocation. Evaluate semantic status, useful progress and recorded next action by reading the files; exact wording is not graded. Cost remains unavailable unless explicitly reported. One execution per case and synthetic projects do not prove general reliability, real-project usefulness or a comparative efficiency improvement.

For normal use, copy only `.agents/skills/mamkin-setup/` and `.agents/skills/mamkin-work/` into a target project's `.agents/skills/`, then ask Codex to use `$mamkin-setup`. Existing target instructions are preserved. Start or continue one task with `$mamkin-work`. No files under `docs/process/`, `.mamkin/` or legacy `.codex/` need to be copied. This stage does not implement autonomous queue/stage traversal.
