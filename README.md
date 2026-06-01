# Universal Vibecode Project Template

A tiny, product-agnostic starting point for vibecode projects. Copy it, ask an init agent to run the setup flow, and the agent will interview you, adapt the docs to the specific product, propose git/GitHub setup, and hand off to a coordinator-led implementation workflow.

The workflow is built for projects run by an init agent, a coordinator/team lead, optional architect, implementation workers, and walkthrough/testing agents. `AGENTS.md` stays short as the agent entrypoint; the durable process lives in `docs/process/`.

## Quick Start

1. Copy this repository for a new project.
2. Ask your agent:

```text
Read AGENTS.md and run the project init flow.
```

3. Answer the init questions.
4. Let the init agent adapt:
   - `README.md`
   - `docs/project/brief.md`
   - `docs/project/decision-log.md`
   - `features/00-roadmap.md`
   - the project-specific agent orchestration notes
5. The init agent verifies git state, proposes GitHub setup, and hands off to the coordinator/team-lead flow.

## Why This Shape

Use `AGENTS.md` as the entrypoint because many coding agents already look for it. Keep it concise so every worker sees only high-signal rules. Put the coordinator manual, role cards, handoff packets, and testing contracts under `docs/process/`.

## Included Files

- `AGENTS.md`: short always-on agent entrypoint.
- `docs/process/init-agent.md`: project initialization protocol and questionnaire.
- `docs/process/agent-orchestration.md`: coordinator/team-lead orchestration manual.
- `docs/process/roles/*.md`: small role cards for non-coordinator worker threads.
- `docs/process/handoff-packets.md`: index of shared packet templates.
- `docs/process/handoff-packets/*.md`: individual kickoff, handoff, defect, retest, and final report templates.
- `docs/project/brief.md`: adapted project source of truth.
- `docs/project/decision-log.md`: durable trace of important decisions.
- `features/00-roadmap.md`: roadmap candidates created or refined during init.
- `docs/templates/feature-spec.md`: feature spec template.
- `docs/templates/walkthrough.md`: coordinator-owned walkthrough/runbook template.

## Design Principles

- Keep `AGENTS.md` short and use it as a pointer to durable process docs.
- Keep live coordination state out of feature specs.
- Require every feature to include product value, acceptance criteria, test plan, manual walkthrough, and human-in-loop gates.
- Use a coordinator-led flow rather than loose worker-to-worker relay.
- Make traceback explicit: project brief -> feature spec -> implementation handoff -> tests -> walkthrough -> follow-ups.
- Treat GitHub/project setup, production actions, secrets, and ambiguous product calls as human approval gates.

## Normal Operating Loop

1. Init agent interviews the human and adapts docs.
2. Coordinator/team lead reviews the project brief and roadmap.
3. Coordinator calls architect to polish architecture and feature boundaries.
4. Coordinator creates or assigns one bounded feature spec and walkthrough definition.
5. Worker implements and returns a handoff packet.
6. Reviewer and/or walkthrough agent verifies the exact branch/commit.
7. Coordinator records results, follow-ups, and the recommended next action.

The goal is a predictable process with enough structure to stay clean, but not so much ceremony that a small project becomes a bureaucracy cosplay.
