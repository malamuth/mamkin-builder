---
name: mamkin-init
description: Initialize a copied Mamkin Builder template. Use for project init, bootstrap interviews, adapting template docs, and starting the Mamkin workflow.
---

# Mamkin Init

Use this skill when a copied Mamkin Builder template should become a concrete project.

## Workflow

1. Read `AGENTS.md`.
2. Read and follow `docs/process/init-agent.md`.
3. Keep the init pass lightweight and interview-driven.
4. Adapt project-facing docs and approved Codex config surfaces only.
5. Do not implement product code during init.
6. Do not create GitHub remotes, external resources, paid services, production systems, MCP/provider config, or secret-dependent setup without explicit human approval.
7. When init is complete, hand off to the coordinator using the packet shape in `docs/process/init-agent.md`.

## Boundaries

- `docs/process/init-agent.md` is the source of truth for init.
- This skill is only a discoverable entrypoint; do not duplicate the full init protocol here.
- If the user asks to improve the template itself, edit the template docs directly instead of running init.
