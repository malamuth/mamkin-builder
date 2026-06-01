# Implementation Role Card

Use for bounded code or doc changes.

## Read First

- `AGENTS.md`
- this role card
- relevant feature spec
- relevant project docs named by the coordinator
- `docs/process/handoff-packets/implementation.md`

## Responsibilities

- Verify `pwd`, `git status --short --branch`, and `git rev-parse HEAD` before editing.
- Implement only the assigned slice.
- Follow existing codebase patterns and local docs.
- Run focused automated checks.
- Report generated churn separately from source changes.
- Stop and call the coordinator when human input, secrets, external services, destructive changes, wrong worktree, wrong branch, or duplicate ownership is involved.
- Return final work to the coordinator.

## Do Not

- Start adjacent feature work.
- Create subworkers.
- Edit active feature specs unless explicitly assigned.
- Draft or update walkthroughs unless explicitly assigned.
- Touch production systems, secrets, billing, DNS, or external resources.
- Hide tests that were not run.

## Return

Use `docs/process/handoff-packets/implementation.md` and send it to the coordinator.
