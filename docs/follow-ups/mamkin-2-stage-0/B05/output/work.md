# Backlog

Order is priority.
T1: discount policy. Blocked: owner has not chosen rate or rounding. No implementation authorized until that decision.
T2: implement discount, depends on T1.
T3: DONE — fix total_cents([]) to return integer 0; preserve nonempty cart behavior. No dependencies.
T4: normalize customer labels. No dependencies.

## Result — 2026-11-10

Completed T3, the highest-priority available task: T1 is blocked by the owner's
decision, and T2 depends on T1. Empty carts now return integer 0. Added a
regression test for the value and exact type; the existing nonempty-cart test
still passes. Check: `python3 -B -m unittest discover -s tests` — 3 tests passed.
Stopped after this task; T4 remains pending.
