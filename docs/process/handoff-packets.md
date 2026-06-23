# Handoff Packets

Use only the packet needed for the current role or handoff. Keep packets self-contained enough that the coordinator can relay them to another thread without rewriting important technical details.

Packets with `Needs human decision`, human-gate blockers, or human/manual steps go back to the coordinator. The coordinator asks the human and records the decision unless the worker prompt explicitly delegated that exact approval lane.

Handoff packets are evidence, not permanent authority. If an older packet conflicts with current human decisions, current source files, current project docs, or a named branch/commit, the coordinator must prefer the current source and mark the old packet detail obsolete.

When a packet makes architecture, source-ownership, generated-artifact, deployment, data, or integration claims, it should name the files, docs, reports, branch/commit, environment, or external proof it relied on. External proof should be described narrowly: what it observed, where, and what it does not prove.

Preferred delivery is direct return to the coordinator thread when the worker prompt provides an exact coordinator thread id and a thread-send tool is available. If direct delivery is unavailable, return the packet in the worker thread starting with `Coordinator handoff - manual relay required` and include the coordinator thread id. The coordinator is responsible for confirming receipt before continuing; a fallback packet is not delivered until it is relayed into the coordinator thread.

`Manual relay required` is a valid completed worker outcome, not a failed handoff. Use it whenever the prompt lacks an exact coordinator thread id or no thread-send tool is available.

Workers must not forward coordinator prompts, create duplicate handoff threads, or send packets to their own worker thread. If a thread-send tool is used, the target `threadId` must be the coordinator thread id from the prompt, never the worker's current thread id, source thread id, or a newly created thread. If the prompt lacks an exact coordinator thread id or no thread-send tool is available, emit the manual-relay packet as the final message in the worker thread.

Every final non-coordinator packet must fill `Coordinator thread id` and `Return path used` so the coordinator can distinguish direct delivery from manual relay.

Coordinators should not poll or read active worker threads while waiting. Continue only after a returned packet/blocker, a human inspection request, or an explicit timeout/recovery step. If a worker has finished but no direct packet arrived, one collection read is allowed to relay the fallback packet.

- Coordinator kickoff: `docs/process/handoff-packets/coordinator-kickoff.md`
- Coordinator final report: `docs/process/handoff-packets/coordinator-final.md`
- Analysis: `docs/process/handoff-packets/analysis.md`
- Architecture: `docs/process/handoff-packets/architecture.md`
- Implementation: `docs/process/handoff-packets/implementation.md`
- Reviewer: `docs/process/handoff-packets/reviewer.md`
- Deployment: `docs/process/handoff-packets/deployment.md`
- UI/UX review: `docs/process/handoff-packets/ux.md`
- Walkthrough defect: `docs/process/handoff-packets/walkthrough-defect.md`
- Walkthrough readiness: `docs/process/handoff-packets/walkthrough-readiness.md`
- Retest request: `docs/process/handoff-packets/retest-request.md`
- Custom role packets: add `docs/process/handoff-packets/<role-name>.md` during init or coordinator-approved setup, using `docs/templates/handoff-packet.md`.
