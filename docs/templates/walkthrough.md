# Feature NN Walkthrough

## Purpose

State what this walkthrough verifies and what it intentionally does not verify.

## Expected Inputs

- Feature spec:
- Branch or commit:
- Required environment:
- Required accounts or services:
- Human actions expected:

Never paste secrets, tokens, magic links, database URLs, or provider keys into chat or docs.

## 1. Verify Worktree

```bash
pwd
git status --short --branch
git rev-parse HEAD
```

Expected result:

- Worktree matches the coordinator prompt.
- Branch/commit matches the implementation handoff.
- Unexpected dirty state is explained before testing.

## 2. Install Or Prepare

Approval gate:

- If this step installs dependencies, accesses the network, creates external resources, changes system/global state, or touches production-like services, stop and get human approval before running commands.

Commands:

```bash
# TBD
```

Expected result:

- Required approval is recorded or this step is confirmed local-only.
- TBD

## 3. Run Automated Checks

Commands:

```bash
# TBD
```

Expected result:

- TBD

## 4. Start Local Services

Commands:

```bash
# TBD
```

Expected result:

- TBD

## 5. Manual Flow

1. TBD
2. TBD
3. TBD

Expected result:

- TBD

## 6. Boundary Flow

1. TBD
2. TBD
3. TBD

Expected result:

- TBD

## 7. Cleanup

Commands or manual cleanup:

```bash
# TBD
```

Expected result:

- Local test artifacts are removed or documented.

## Result Packet

```text
Status: Merge-ready | Verified with follow-ups | Not merge-ready
Role: walkthrough
Feature/Slice:
Tested worktree:
Tested branch:
Tested commit:
Automated checks:
Manual checks:
Deployment checks:
Known follow-ups:
Generated churn observed:
Docs updated:
Merge recommendation:
```
