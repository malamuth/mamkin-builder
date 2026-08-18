# Adaptive Model Routing

Use this protocol before launching delegated work. Choose role, reasoning profile, and access posture independently. The role owns the responsibility and packet; the profile owns model effort; access owns the sandbox. Task size alone does not select a stronger profile.

## Profiles

| Profile | Model and effort | Default use |
| --- | --- | --- |
| Economy | `gpt-5.6-terra` / `medium` | Bounded read-only inventory, extraction, classification, or mechanical verification with a deterministic oracle. Luna/low remains an experiment candidate after failing the current same-case quality gate. |
| Balanced | `gpt-5.6-terra` / `medium` | Reversible, well-specified implementation, deployment, testing, and ordinary analysis. |
| Deep | `gpt-5.6-sol` / `high` | Conflicting sources, architecture tradeoffs, shared contracts, cross-component work, unknown root cause, nondeterministic validation, or material product judgment. |
| Critical | `gpt-5.6-sol` / `xhigh` | Security/auth boundaries, payments, production data or incidents, destructive migrations, irreversible external state, or concurrency correctness. |

Never select `max` automatically. It requires a human choice or accepted same-case evidence that `xhigh` is insufficient. The selector does not emit a `max` preset; an approved exceptional launch is runtime-specific and must be recorded in the assignment and experiment log.

## Deterministic Selection

Classify observable signals, then run:

```bash
python3 scripts/select_model_profile.py \
  --role reviewer \
  --access read-only \
  --signal shared-contract
```

Critical signals establish a `critical` floor; deep signals establish a `deep` floor. Economy requires read-only access plus every configured economy requirement. Everything else starts balanced. A requested profile may raise the result but never lower its risk floor.

The selector returns the exact profile preset. Profile presets deliberately contain no role identity: the worker prompt must still name one role card and packet. Use an existing role preset only as a compatibility fallback when it meets or exceeds the selected floor. If the selected preset or model is unavailable, stop and report it; never silently downgrade critical or deep work.

## Escalation And De-escalation

Escalate only on new evidence:

- two focused attempts fail without explaining the cause;
- requirements or authoritative sources conflict;
- scope crosses a component or shared contract;
- the validation oracle becomes nondeterministic or insufficient; or
- a critical signal appears.

Return the current profile, requested profile, trigger, evidence, and next bounded action. The coordinator decides whether to relaunch; workers do not silently change models. Do not escalate merely because a task is long or a test is slow.

After architecture or diagnosis resolves the uncertainty, route the next bounded implementation independently and allow a lower profile when its remaining risk floor permits it. Acceptance selects its own profile and remains independent from implementation.

## Evaluation

Use the model-routing cases in `evals/mamkin-prompt-cases.json` and the hard quality gate in `evals/mamkin-role-model-matrix.json`. Compare adjacent profiles on the same state. Record success, missed or unsupported findings, permissions, validation, handoff, correction turns, latency, tokens, tool calls, and cost when available. A cheaper profile is accepted only when every hard dimension passes.
