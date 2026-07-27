# Thread Operations And Recovery

Read this only when starting, receiving from, or recovering a separate worker task. Normal role behavior, execution-mode selection, and the worker handoff invariant live in `AGENTS.md` and `docs/process/execution-lane-routing.md`; this file owns coordinator-side task mechanics.

## Start A Clean Lane

- Create a clean thread with a standalone role prompt. Do not fork the coordinator for implementation, walkthrough, review, deployment, or specialist work unless the human explicitly wants inherited coordinator history.
- Use the matching `.codex/agents/mamkin-*.toml` preset when supported.
- Include the exact thread name, coordinator thread id, worktree, branch or commit, allowed files, goal, success criteria, validation, output packet, and stop rule.
- Confirm that a separate-task trigger from `docs/process/execution-lane-routing.md` applies and declare the prompt's execution mode. Do not create a durable task for work that passed every subagent condition unless persistence or user visibility is the reason.

After creation, perform one bounded start-health check. Treat the lane as failed to start when it has no visible turn content, contains inherited coordinator/reset history instead of the standalone role prompt, or cannot be resolved consistently by available thread tools. Mark the id superseded, try at most one replacement when useful, then use a manual starter prompt. Re-evaluate execution mode before any fallback; task-creation failure does not make independent or long-lived work suitable for a subagent.

## Receive A Packet

The dynamic worker prompt owns the exact return path. Direct thread send is preferred when the coordinator id and tool are available. Manual relay is an expected fallback, not a failed worker outcome.

Do not poll or summarize an active worker lane. With two tracks, packets may return in either order and one blocker does not stop the other unless a shared assumption changes. Continue after a returned packet or blocker, a human inspection request, or an explicit timeout/recovery step. If the worker has finished but direct delivery did not arrive, perform one collection read and relay the fallback packet.

Confirm receipt before routing follow-up work. Old packets are evidence only and never override current human decisions or current sources.

## Recovery Cases

- If a worker sends to itself, recover the packet once, restate the exact coordinator target, and do not duplicate the lane.
- If a worker or walkthrough inherits coordinator/reset context, supersede it and create a clean standalone lane.
- If thread tools cannot create or deliver reliably, return the exact standalone starter prompt for human paste and report the limitation.
- If the coordinator begins monitoring or implementing inside an active lane, stop and return to the coordinator/worker ownership boundary.

## Coordinator Rollover

Coordinator rollover is not an ordinary worker-thread recovery path. Use `.agents/skills/mamkin-coordinator-rollover/SKILL.md` and `docs/process/handoff-packets/coordinator-reset.md` after human approval.
