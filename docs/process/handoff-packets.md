# Handoff Packets

Use only the packet needed for the current role or handoff. Keep packets self-contained enough that the coordinator can relay them to another thread without rewriting important technical details.

Packets with `Needs human decision`, human-gate blockers, or human/manual steps go back to the coordinator. The coordinator asks the human and records the decision unless the worker prompt explicitly delegated that exact approval lane.

Handoff packets are evidence, not permanent authority. If an older packet conflicts with current human decisions, current source files, current project docs, or a named branch/commit, the coordinator must prefer the current source and mark the old packet detail obsolete.

When a packet makes architecture, source-ownership, generated-artifact, deployment, data, or integration claims, it should name the files, docs, reports, branch/commit, environment, or external proof it relied on. External proof should be described narrowly: what it observed, where, and what it does not prove.

Workers follow the Worker Handoff Contract in `AGENTS.md` and the exact path in their task prompt. Every separate-task packet fills `Coordinator thread id` and `Return path used`. A subagent fills `Parent lane owner`, returns once to that parent, and does not perform a separate coordinator delivery. Coordinator-side delivery and recovery mechanics live in `docs/process/thread-operations.md`.

- Coordinator kickoff: `docs/process/handoff-packets/coordinator-kickoff.md`
- Coordinator reset/rollover: `docs/process/handoff-packets/coordinator-reset.md`
- Coordinator final report: `docs/process/handoff-packets/coordinator-final.md`
- Analysis: `docs/process/handoff-packets/analysis.md`
- Architecture: `docs/process/handoff-packets/architecture.md`
- Implementation: `docs/process/handoff-packets/implementation.md`
- Reviewer: `docs/process/handoff-packets/reviewer.md`
- Deployment: `docs/process/handoff-packets/deployment.md`
- Designer: `docs/process/handoff-packets/designer.md`
- UI/UX review: `docs/process/handoff-packets/ux.md`
- Walkthrough defect: `docs/process/handoff-packets/walkthrough-defect.md`
- Walkthrough readiness: `docs/process/handoff-packets/walkthrough-readiness.md`
- Retest request: `docs/process/handoff-packets/retest-request.md`
- Project evolution audit: `docs/process/handoff-packets/project-evolution-audit.md`
- Custom role packets: add `docs/process/handoff-packets/<role-name>.md` during init or coordinator-approved setup, using `docs/templates/handoff-packet.md`.
