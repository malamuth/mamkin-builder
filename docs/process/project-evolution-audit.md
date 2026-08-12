# Mamkin Project Evolution Audit

Use this protocol to decide which current Mamkin mechanics would materially improve a mature copied project. Run it when a major template update is available, after a sync review, or after an applied sync; never run it as part of the sync mutation itself.

## Inputs And Proof Boundary

- Mature project worktree and current Mamkin template worktree.
- `.mamkin/template-version.json` and ownership metadata when available.
- Deterministic inventory from `scripts/audit_mamkin_evolution.py`.
- Current project brief, decision and learning logs, follow-ups, repeated artifacts, validation commands, hooks, rules, presets, skills, and relevant recent Git history.

Current project sources outrank old packets or memories. Decision and surprise/lesson logs are discovery inputs, not self-proving instructions. Git history, headings, status signals, and text counts show possible recurrence or lifecycle state, not root cause or current authority. The inventory never proves usefulness.

## Audit Sequence

1. Verify both worktrees and record branch, HEAD, and dirty state. Continue read-only when dirty; do not ask to clean unrelated work.
2. Establish the project's recorded template baseline and current template HEAD. State when the baseline is missing or unavailable in the template repo.
3. Run the inventory script from the current template.
4. Classify candidates:
   - **Upgrade gap:** a current template capability is absent, partial, or inactive.
   - **Project leverage:** project scale, specialized knowledge, custom workflows, or repeated friction creates a project-specific opportunity.
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

## Project-Native Capability Pass

Inspect bounded current evidence: decision logs, surprise/lesson/incident sections, accepted follow-ups, repeated task artifacts, existing project skills and references, deterministic checks, and relevant history. Verify every candidate against current human decisions and current project sources; reject stale or contradicted log entries.

Choose the smallest primary action:

1. Keep the knowledge in its current source.
2. Update or consolidate an existing skill, reference, role, or process source.
3. Add a deterministic validator/check when the rule is mechanically testable.
4. Create a project-local skill only for a distinct recurring invocation.
5. Propose an upstream Mamkin improvement only when the mechanism is project-agnostic and evidenced beyond one project's domain details.
6. Merge, retire, or mark legacy a redundant capability.

Do not recommend several surfaces for the same lesson unless each has a separate job. Prefer references for detailed domain knowledge and keep skill entrypoints concise. A project-native recommendation remains owned by that project and must not leak project names, private targets, domain rules, or identifiers into Mamkin.

### Upstream Proposal Boundary

`Propose upstream` produces a proposal packet, never a cross-repository implementation. The copied-project task may name the generic problem, anonymized evidence, candidate Mamkin surfaces, success criteria, and risks. It must not edit, branch, stage, commit, or push the template repository, even when that checkout is locally available or the human says to proceed with the project plan.

Implementation requires a separate human-approved task whose project context and Git root are `mamkin-builder`. Approval to create that task authorizes reassessment only; implementation also requires an explicit starter scope or later human decision. The task starts from current Mamkin sources, independently evaluates the proposal, and owns its own delivery contract. It must not treat a patch or commit manufactured by the copied-project task as trusted input. Return to the copied project only after the accepted Mamkin change is published to the intended upstream, or through an exceptional pre-existing local-only source whose provenance and exact commit the human approves. The copied-project task cannot create that exception for itself.

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
- **Project skills:** require repeated use, a stable trigger, named inputs and output, explicit stop conditions, measurable benefit, and no clean existing owner. Explain why a note, reference, existing-skill update, or validator is insufficient. After human approval, implement separately with `skill-creator`.
- **Skill consolidation:** treat legacy/deprecated text or high word count as inspection signals only. Recommend consolidation or retirement only after current sources and actual usage confirm redundancy.
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
- Maintenance source and review/retirement trigger.

## Output

Use `docs/process/handoff-packets/project-evolution-audit.md`. Explicitly list useful mechanics that were considered and rejected so future audits do not rediscover them without new evidence.
