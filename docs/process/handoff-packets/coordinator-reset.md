# Coordinator Reset Packet

Use this when rolling over from a long, drifting, or context-heavy coordinator thread into a fresh coordinator thread.

```text
Status: Coordinator reset ready | Needs human decision | Blocked
Reason for reset:
Old coordinator thread id:
New coordinator thread id, if known:
Worktree:
Branch:
Baseline commit or exact state:
Source authority:
Current model:
Obsolete or unsafe assumptions:
Active lanes:
Dirty repos/worktrees:
External proof boundary:
Next safe action:
Must not do next:
Human gates:
Docs updated:
```

The fresh coordinator's first action should be an architecture restatement from this packet and current repo files. A new Git branch is not required for rollover unless the next slice will write files or needs isolated ownership.
