# Coordinator Reset Packet

Use this when rolling over from a long, drifting, or context-heavy coordinator thread into a fresh coordinator thread.

```text
Status: Coordinator reset ready | Needs human decision | Blocked
Reason for reset:
Old coordinator thread id:
New coordinator thread id, if known:
Rollover execution path: Created/sent by coordinator | Manual fallback required
Main coordinator after rollover:
Worktree:
Branch:
Baseline commit or exact state:
Source authority:
Current model:
Obsolete or unsafe assumptions:
Active lanes:
Managed portfolio registry/generation and child ledger references, if applicable:
Transfer packet and successor receipt, if applicable:
Managed parent old/new identity, generation and recovery-route reconciliation, if applicable:
Dirty repos/worktrees:
External proof boundary:
Next safe action:
Must not do next:
Human gates:
Starter prompt sent:
Fresh coordinator receipt verified:
Old coordinator archived/renamed:
Old coordinator final status:
Docs updated:
```

The fresh coordinator's first action should be an architecture restatement from this packet and current repo files. A new Git branch is not required for rollover unless the next slice will write files or needs isolated ownership.

When thread-management tools are available and rollover is approved, the outgoing coordinator should create or start the fresh coordinator thread, send the starter prompt, verify receipt when possible, archive/rename itself, and promote the fresh thread as the main coordinator. Manual fallback is only for missing or blocked thread tools.

Parent-led child transfer uses `docs/process/managed-projects.md` and `docs/templates/coordinator-transfer.json`. A matching receipt and reconciled authority are required before resuming. Rename/stop the old task first; archive only after a separate closeout preflight proves its worktree has no live dependents and needed evidence is preserved. Parent rollover carries the complete child registry and outstanding recovery ownership.
