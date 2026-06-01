# Handoff Packets

Use only the packet needed for the current role or handoff. Keep packets self-contained enough that the coordinator can relay them to another thread without rewriting important technical details.

Packets with `Needs human decision`, human-gate blockers, or human/manual steps go back to the coordinator. The coordinator asks the human and records the decision unless the worker prompt explicitly delegated that exact approval lane.

If no explicit thread-delivery tool or return path is delegated, return the packet in the worker thread and label it `Coordinator handoff`. The coordinator is responsible for collecting or pasting it into the coordinator thread.

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
