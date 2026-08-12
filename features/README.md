# Features

This folder contains coordinator-owned feature specs.

Init creates or updates only `features/00-roadmap.md`. After init, the coordinator and planning lane turn roadmap candidates into feature specs.

Naming:

- Roadmap: `features/00-roadmap.md`
- Feature specs: `features/NN-short-kebab-title.md`

Feature specs should be stable once implementation starts. Record completed walkthrough notes or non-blocking follow-ups under `docs/follow-ups/`, not inside active feature specs.

Before implementation, each spec declares the Git delivery contract from `docs/process/git-delivery.md`. Named feature branches are the default; the coordinator owns integration and cleanup after independent acceptance.
