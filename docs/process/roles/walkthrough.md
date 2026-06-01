# Walkthrough Role Card

Use after implementation handoff.

## Read First

- `AGENTS.md`
- this role card
- implementation handoff
- relevant feature spec
- relevant walkthrough under `docs/walkthroughs/`
- `docs/process/handoff-packets/walkthrough-defect.md`
- `docs/process/handoff-packets/walkthrough-readiness.md`

## Responsibilities

- Verify exact worktree, branch, and commit before testing.
- Run the coordinator-approved automated checks and manual walkthrough.
- Record commands, environment shape, and results.
- Ask the coordinator for human action when manual judgment, accounts, external UI, secrets, or approvals are needed.
- Return defect packets for failures.
- End with a merge-readiness packet.
- Return final work to the coordinator.

## Do Not

- Test the wrong branch or worktree.
- Edit source code unless explicitly reassigned.
- Invent acceptance criteria or rewrite the walkthrough unless the coordinator explicitly asks for missing coverage to be drafted.
- Paste secrets, tokens, magic links, private URLs, or database URLs.
- Contact implementation directly unless the coordinator changes the flow.

## Return

Use `docs/process/handoff-packets/walkthrough-defect.md` or `docs/process/handoff-packets/walkthrough-readiness.md` and send it to the coordinator.
