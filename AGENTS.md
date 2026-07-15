# Agent Notes

## Request Routing

- Improve the template itself by editing template files directly; do not run project init. Prompt, role, hook, or reasoning changes also follow `docs/process/prompt-evals.md`.
- Initialize or adapt a copied project with `.agents/skills/mamkin-init/SKILL.md` and `docs/process/init-agent.md`.
- Coordinate feature or multi-agent work with `.agents/skills/mamkin-coordinate/SKILL.md` and `docs/process/agent-orchestration.md`.
- Audit coordinator drift with `.agents/skills/mamkin-context-audit/SKILL.md`; run an approved same-thread reset or rollover with the matching Mamkin skill.
- Update a copied project's process layer with `.agents/skills/mamkin-template-sync/SKILL.md`.
- Assigned workers read their role card under `docs/process/roles/`, the relevant feature or walkthrough, and only the packet they must return.
- Product context lives in `docs/project/brief.md`, `docs/project/decision-log.md`, relevant `features/*.md`, and `docs/walkthroughs/`.

## Project Commands

Fill these during init once the stack is known. Until then, do not invent commands; report that project commands are not configured.

- Setup/install: TBD
- Run locally: TBD
- Check before handoff: TBD

## Autonomy And Human Gates

- For answer, review, diagnose, audit, or planning requests, inspect relevant material and report; do not implement unless the request asks for changes.
- For change, build, or fix requests, make in-scope local edits and run relevant non-destructive checks without asking first.
- Stop for human confirmation before external writes or resources, remotes or pushes, paid services, production actions, DNS, public posting, destructive migrations, secrets or production data, scope/privacy/public-behavior tradeoffs, provider or MCP setup, weakening Codex restrictions, or system/global tooling and local service installation.
- In copied projects, inherited Git state and remotes are `TBD` until the human approves a project-specific target. Never use a template remote for project/product pushes.
- If a command needs credentials, use only an explicitly approved local/provider secret path or variable names, and do not print or store secret values.

## Repository Safety And Evidence

- Before implementation, run `pwd`, `git status --short --branch`, and `git rev-parse HEAD`.
- Preserve user changes and explain unexpected dirty state.
- Current human decisions and current repo sources outrank old packets, summaries, memory, generated reports, screenshots, and external checks. State the narrow proof boundary of external evidence.
- Multiple write-capable agents must use separate worktrees or explicitly disjoint file ownership.
- Keep reusable process in `docs/process/`; keep project plans and state in `docs/project/`, `features/`, `docs/walkthroughs/`, or `docs/follow-ups/`.
- Keep active feature specs stable during implementation unless spec editing is explicitly assigned.
- Run relevant validation before completion, or report what could not be run and the next best check.
- Project-local `.codex` config, hooks, rules, and presets load only when the project is trusted; changed hooks may need review. Runtime permissions can be broader than preset defaults, but they do not override these human gates or file ownership.

## Worker Handoff Contract

- The coordinator owns human decisions unless the worker prompt delegates one exact question.
- Every worker prompt must provide the coordinator thread id and exact handoff path. Use direct thread send when available; otherwise return one final packet beginning `Coordinator handoff - manual relay required for coordinator thread <id>`.
- Never send the packet to the worker's own thread through a thread-send tool, forward the coordinator prompt, or create a duplicate handoff thread. Return one packet, then stop.
- Write-capable implementation and acceptance walkthroughs use separate Codex lanes/threads by default. A same-thread subagent exception requires explicit human approval for that task.
