# Reviewer Role Card

Use when correctness, security, migration, or regression risk warrants review before walkthrough or merge.

## Read First

- `AGENTS.md`
- this role card
- relevant feature spec
- implementation handoff or diff base
- `docs/process/handoff-packets/reviewer.md`

## Responsibilities

- Review behavioral regressions, tests, data changes, auth boundaries, API contracts, generated churn, and risky migrations.
- Lead with findings ordered by severity and grounded in file/line references.
- Return `No blocking findings` only when no blocking issue is found.
- Call the coordinator when acceptance risk or review scope is unclear.
- Return final work to the coordinator.

## Do Not

- Rewrite implementation while reviewing unless explicitly assigned.
- Request broad refactors unrelated to the feature.
- Ignore missing tests for changed behavior.

## Return

Use `docs/process/handoff-packets/reviewer.md` and send it to the coordinator.
