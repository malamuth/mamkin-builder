# Agent Notes

## Request Routing

- If asked to improve this template itself, edit the template docs directly; do not run the project init flow.
- If asked to initialize, adapt, or start a copied project from this template, read and follow `docs/process/init-agent.md`.
- If asked to coordinate feature work or multi-agent work, read `docs/process/agent-orchestration.md`.
- If assigned a worker or specialist role, read the matching role card in `docs/process/roles/` instead of the full orchestration manual.
- For product context, read `docs/project/brief.md`, `docs/project/decision-log.md`, the relevant `features/*.md`, and any relevant walkthrough in `docs/walkthroughs/`.

## Project Commands

Fill these during init once the stack is known. Until then, do not invent commands; report that project commands are not configured yet.

- Setup/install: TBD
- Run locally: TBD
- Check before handoff: TBD

## Hard Rules

- Involve the human before creating GitHub projects, remotes, paid resources, external services, production deployments, or DNS changes.
- In copied projects, treat inherited Git state and remotes as `TBD` until the human approves a project-specific target. A template repo remote is not a valid push target for project/product commits.
- Involve the human before adding or enabling MCP servers, connectors, provider integrations, or project config that reaches external services or starts local services.
- Involve the human before weakening `.codex` sandbox, approval, hooks, rules, network, or shell environment restrictions.
- Involve the human before touching secrets, tokens, billing, production data, destructive migrations, or public posting.
- Involve the human before product tradeoffs that change scope, audience, privacy, data retention, or public behavior.
- Involve the human before installing or changing system/global tooling, local databases/services, Docker/Colima, Homebrew packages, language runtimes, or other machine-level setup.
- Check `pwd`, `git status --short --branch`, and `git rev-parse HEAD` before implementation work.
- Do not overwrite user changes. Work with unexpected dirty state and report surprises.
- When facts conflict, treat current human decisions and current repo sources/docs as authority. Old handoff packets are historical evidence, not source of truth.
- Do not store secrets, magic links, private URLs, tokens, provider keys, or database URLs in repo docs or chat.
- If a command needs secrets, use a human-approved local/provider secret path; do not rely on inherited shell secrets unless the coordinator explicitly approves the variable names and the command will not print them.
- If multiple write-capable agents run in parallel, use separate worktrees or explicitly disjoint allowed file ownership.
- Keep process docs generic. Put project planning in `docs/project/`, `features/`, or `docs/follow-ups/` unless changing reusable workflow rules.
- If a non-coordinator agent hits a human decision gate, return it to the coordinator unless the prompt explicitly delegates asking the human in that thread.
- Use the assigned handoff return path. If the prompt provides an exact coordinator thread id and a thread-send tool is available, send the packet directly to that coordinator thread. Otherwise start the local packet with `Coordinator handoff - manual relay required`.
- Coordinators should not monitor active worker threads. Wait for an explicit returned packet, a blocker, or a human request to inspect.
- Coordinators should not do implementation, inventory, or content work inline once a feature lane exists. Route additional work to the existing implementation thread when appropriate, or start a new worker with explicit file ownership.
- If a coordinator repeats corrected facts, loses source ownership, over-focuses on stale details, or starts reasoning from memory in a complex lane, pause execution and run a source-grounded context reset or architect check before continuing.
- A fresh coordinator thread does not require a fresh Git branch. Use a committed coordinator reset packet as the new thread baseline; create a branch/worktree only for the next write-capable slice when isolation is needed.
- Run appropriate checks before declaring work done, or clearly report what was not run.
- Record durable project decisions in `docs/project/decision-log.md`; use the Surprise Log only for agent mistakes and confusion points.
- Keep active feature specs stable once implementation starts. Put completed test notes and non-blocking follow-ups under `docs/follow-ups/`.

## Surprise Log

Below are common agent mistakes and confusion points in this repository. If you encounter something surprising while working, alert the developer and add a concise note to the Surprise Log for a future agent.

- Worker packets may remain in the worker thread when direct thread delivery is unavailable. This is not a failed worker handoff if the packet starts with `Coordinator handoff - manual relay required`; the coordinator should do one receipt-recovery read and relay it. Worker prompts and presets must also say not to forward prompts or send packets to the worker's own thread.
