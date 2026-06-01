# Agent Notes

## Request Routing

- If asked to improve this template itself, edit the template docs directly; do not run the project init flow.
- If asked to initialize, adapt, or start a copied project from this template, read and follow `docs/process/init-agent.md`.
- If asked to coordinate feature work or multi-agent work, read `docs/process/agent-orchestration.md`.
- If assigned a worker or specialist role, read the matching role card in `docs/process/roles/` instead of the full orchestration manual.
- For product context, read `docs/project/brief.md`, `docs/project/decision-log.md`, the relevant `features/*.md`, and any relevant walkthrough in `docs/walkthroughs/`.

## Hard Rules

- Involve the human before creating GitHub projects, remotes, paid resources, external services, production deployments, or DNS changes.
- Involve the human before touching secrets, tokens, billing, production data, destructive migrations, or public posting.
- Involve the human before product tradeoffs that change scope, audience, privacy, data retention, or public behavior.
- Check `pwd`, `git status --short --branch`, and `git rev-parse HEAD` before implementation work.
- Do not overwrite user changes. Work with unexpected dirty state and report surprises.
- Do not store secrets, magic links, private URLs, tokens, provider keys, or database URLs in repo docs or chat.
- Keep process docs generic. Put project planning in `docs/project/`, `features/`, or `docs/follow-ups/` unless changing reusable workflow rules.
- If a non-coordinator agent hits a human decision gate, return it to the coordinator unless the prompt explicitly delegates asking the human in that thread.
- Run appropriate checks before declaring work done, or clearly report what was not run.
- Record durable project decisions in `docs/project/decision-log.md`; use the Surprise Log only for agent mistakes and confusion points.
- Keep active feature specs stable once implementation starts. Put completed test notes and non-blocking follow-ups under `docs/follow-ups/`.

## Surprise Log

Below are common agent mistakes and confusion points in this repository. If you encounter something surprising while working, alert the developer and add a concise note to the Surprise Log for a future agent.

- No surprises recorded yet.
