# Context Health Audit

Use this read-only protocol when a coordinator thread may be drifting, contaminated by stale packets, or reasoning from memory instead of current sources.

The audit does not run context reset or rollover by itself. It classifies the situation and returns the smallest safe escalation.

## Statuses

Use one status:

- `OK`: continue normal coordination.
- `watch`: proceed, but record the risk and the trigger that would require reset.
- `context reset recommended`: pause action in the same coordinator thread and produce a source-grounded restatement before continuing.
- `rollover recommended`: create a fresh coordinator thread from a reset baseline using the coordinator rollover process.

When using Codex skills, `context reset recommended` maps to `mamkin-context-reset`, and `rollover recommended` maps to `mamkin-coordinator-rollover`.

## Watch

`watch` means the thread is not bad enough to reset yet, but the next coordinator action should be cautious and source-grounded.

Use `watch` for cases like:

- One stale assumption was made and corrected after reading current docs.
- A worker packet had ambiguous evidence, but no unsafe action was taken.
- The thread is getting long, but recent recommendations still cite current sources.
- There is a dirty worktree or old-packet risk, but no source confusion has appeared yet.

Every `watch` result must include an explicit trigger, for example:

```text
Status: watch
Reason: Coordinator referenced an old packet once, then corrected after reading current docs.
Trigger: If the coordinator repeats stale source ownership or recommends implementation without restatement, run context reset.
```

## Context Reset Versus Rollover

Use context reset when the same coordinator thread is still usable. The coordinator pauses work, reads authoritative files, and returns a source-grounded restatement before routing or implementing anything else.

Use rollover when the current coordinator has become structurally unreliable. Rollover promotes a fresh coordinator thread from a committed reset baseline and archives or renames the outgoing coordinator.

## Evidence To Inspect

Read only what is needed:

- `AGENTS.md`
- `docs/process/agent-orchestration.md`
- `docs/process/handoff-packets/coordinator-reset.md`
- `docs/project/decision-log.md`
- Relevant feature specs, roadmap entries, follow-ups, and walkthroughs.
- Current `git status --short --branch` and `git rev-parse HEAD`.
- Recent coordinator messages or returned packets when thread tooling is available and the human asked to inspect them.

Do not treat old handoff packets, old summaries, generated reports, or screenshots as authoritative unless current docs confirm them.

## Escalation Signals

Prefer `context reset recommended` when:

- The coordinator made a stale or contradictory claim but can still correct course.
- Current source authority is unclear.
- Dirty worktrees, old packets, or generated reports are competing with current docs.
- A feature lane needs an architecture restatement before more work.
- The coordinator started answering from memory but has not repeated the mistake after correction.

Prefer `rollover recommended` when:

- Corrected facts are repeated incorrectly.
- The coordinator invents a model or source ownership instead of reading sources.
- The coordinator keeps over-focusing on stale details after correction.
- Old packets or summaries override current files or human decisions.
- The coordinator starts implementation, live validation, or worker routing after a stop/reset instruction.
- The thread is so long or polluted that further inline repair would likely add more confusion.

## Output Packet

Return this packet:

```text
Status: OK | watch | context reset recommended | rollover recommended
Worktree:
Branch:
HEAD:
Sources read:
Current authority:
Contamination evidence:
Stale or unsafe assumptions:
External proof boundary:
Recommended next action:
Watch trigger, if any:
Reset required before:
Rollover baseline needed:
Human decision needed:
Tests/checks run:
```
