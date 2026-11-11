# Mamkin 2.0 Stage 2 checks

The product remains two skills. This directory is evaluation material for [the Stage-2 contract](../../../docs/project/mamkin-2-stage-2.md); no selector script or scheduler is installed in target projects.

`cases.py` freezes 18 requests and initial Markdown plans. Tasks produce inert named text artifacts and an ordered completion journal. Parent checks compare actual output sets, literal contents, completion order, preserved user files and absence of the publication marker. The journal is part of these synthetic task outcomes, not a required Mamkin runtime file. Source skills, tools and unrelated files must remain unchanged.

Backlog tests cover default one-task scope, priority/ties, blocked items, dependency unlocking and a completed queue. Sequential tests cover mandatory blocking, separate human exit gates, optional remainder, a named phase boundary and explicit next-phase permission. Hybrid can skip a local blocker but cannot cross the phase. Count limits are tested with actual partial work on the final admitted ID and fresh-chat continuation; another continuation cannot admit a third ID. Invalid graphs and an expired fixed deadline must stop without invented resolution or renewed authority. A local publish stub detects prohibited command execution without contacting external resources. Setup must preserve a suitable existing hybrid plan byte-for-byte.

Each request runs in a fresh `codex exec --ephemeral` with the installed CLI, requested `gpt-6.1-sol/high`, workspace-write and ordinary approvals/rules. Shared groups carry only actual project files between invocations; no prior responses or conversation are supplied. No provider, credential or user-level configuration changes are made. Runtime launcher permission may be needed on this host.

Run only after freezing source and criteria in Git:

```sh
python3 -B evals/mamkin-2/stage-2/run.py --output /private/tmp/mamkin-2-stage-2-new-run
```

The runner refuses an existing output directory and exits nonzero on a failed/incomplete case. It never executes model-created code in the parent: acceptance reads inert files. Semantic statuses, gates, grant limits, blockers and plan preservation are reviewed separately against actual files/commands; automated file checks do not issue an overall behavioral pass. Known preparation scripts are local standard-library fixtures, not new product dependencies.

Re-run the unchanged Stage-1 sequence with the final two skills for regression. Preserve source hashes, actual final responses, meaningful changed output/state, failed attempts, deterministic checks and separately reviewed behavioral results. Keep raw streams temporary and retain compact evidence for no-op/blocked cases. One sample per case, synthetic projects and recorded command events do not establish real-project reliability, hard resource enforcement or an efficiency gain.

## Versioned Stage-1 regression coverage

The first legacy-regression attempt stopped at S04 because the agent expanded `test_label` into a table containing the original Ada assertion plus additional cases. The old AST-body preservation check failed although the behavior, independent oracle and unit suite passed. That failed legacy verdict is retained and is never rescored.

`regression.py` version 2 reuses every unchanged Stage-1 request and fixture, leaving the frozen Stage-1 files intact. It replaces only AST-body identity with executed semantic coverage controls: the normal unit suite must pass, a mutation of the original Ada label must produce assertion failures, and an off-by-one mutation restricted to the original multi-item input `[(125,2),(50,1)]` must produce assertion failures. Import/runtime errors do not count as catching a mutation. These probes run inside the same read-only, network-disabled native sandbox. The old AST result is also retained diagnostically. All other preservation, code, pause/resume and permission criteria remain unchanged.

Freeze this wrapper before its fresh model sequence, then run `python3 -B evals/mamkin-2/stage-2/regression.py --output /private/tmp/mamkin-2-stage-2-new-regression`. This is a new evaluation contract, not a retroactive pass for the original stopped attempt.
