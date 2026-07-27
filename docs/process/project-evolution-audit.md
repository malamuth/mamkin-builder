# Mamkin Project Evolution Audit

Use this protocol to decide which current Mamkin mechanics would materially improve a mature copied project. Run it when a major template update is available, after a sync review, or after an applied sync; never run it as part of the sync mutation itself.

## Inputs And Proof Boundary

- Mature project worktree and current Mamkin template worktree.
- `.mamkin/template-version.json` and ownership metadata when available.
- Deterministic inventory from `scripts/audit_mamkin_evolution.py`.
- Current project brief, decision log, follow-ups, validation commands, hooks, rules, presets, skills, and relevant recent Git history.

Current project sources outrank old packets or memories. Git history and text-signal counts show recurrence, not root cause. The inventory proves presence, absence, or activation state only; it does not prove usefulness.

## Audit Sequence

1. Verify both worktrees and record branch, HEAD, and dirty state. Continue read-only when dirty; do not ask to clean unrelated work.
2. Establish the project's recorded template baseline and current template HEAD. State when the baseline is missing or unavailable in the template repo.
3. Run the inventory script from the current template.
4. Classify candidates:
   - **Upgrade gap:** a current template capability is absent, partial, or inactive.
   - **Project leverage:** project scale, custom workflows, or repeated friction creates a project-specific opportunity.
   - **Redundancy:** an old project mechanism duplicates or conflicts with the current protocol.
   - **No-fit:** a capability is absent but has no demonstrated project value.
5. Read only the project evidence needed to evaluate plausible candidates.
6. Score, filter, and render the audit packet in the response. Do not write the packet or apply recommendations.

A dirty or unverified template may support capability assessment, but it is not an executable sync source. Make the next sync action conditional on a committed, clean template whose reviewed HEAD is verified against the intended upstream or explicitly approved as local-only.

## Evidence Gate

A recommendation needs at least one:

- Two or more concrete occurrences of the same friction or manual workaround.
- One high-impact safety, recoverability, ownership, or external-action gap.
- A deterministic prerequisite missing from a project with multiple prior process updates or substantial project-specific process customization.
- A measured prompt, latency, validation, or handoff regression that the mechanic directly addresses.

Do not recommend a hook, model change, new role, extra document, or automation because it exists upstream. Name exact evidence and its source.

## Profitability Score

Score each candidate:

```text
Benefit = recurrence (0-3) + time/token saving (0-3) + risk reduction (0-3) + project fit/confidence (0-2)
Cost = adoption effort (0-3) + ongoing maintenance (0-3)
Net value = Benefit - Cost
```

Classify:

- **Adopt now:** evidence gate passes, net value at least `6`, success is measurable, and rollback is clear.
- **Bounded experiment:** evidence gate passes, net value `3-5`, uncertainty is material, and the test is reversible with a named stop condition.
- **Do not adopt:** evidence gate fails, net value is below `3`, an equivalent already exists, or maintenance exceeds likely benefit.

Recommend at most five adopt-now items. Prefer one smaller mechanism with direct evidence over a broad process package.

## Mechanic-Specific Gates

- **Hooks:** require a deterministic trigger, repeat-safe command, bounded timeout, visible failure, no secret output, and a project trust/reload note.
- **Validation:** require a real project command or deterministic check; never invent one from the stack.
- **Models/reasoning:** require same-case quality evals. Keep high-risk roles at their current setting without role-specific evidence.
- **Subagents/tasks:** require observable routing triggers and preserved implementation/acceptance separation.
- **New roles/docs:** require repeated responsibility that existing roles or project sources cannot own cleanly.
- **Sync/metadata:** preserve mixed and project-owned files; route file transfer through `mamkin-template-sync`.
- **External tools/providers:** recommendation may describe value, but setup remains a separate human-approved action.

## Success And Rollback

Each adopt-now or experiment item must name:

- Exact files or runtime surface affected.
- Expected benefit and one observable success measure.
- Validation required after adoption.
- Review date or event.
- Rollback or disable path.
- Human decision or trust/restart action, if any.

## Output

Use `docs/process/handoff-packets/project-evolution-audit.md`. Explicitly list useful mechanics that were considered and rejected so future audits do not rediscover them without new evidence.
