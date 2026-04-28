# Failure-Mode Taxonomy

Audience: anyone maintaining or extending the failure taxonomy. The 14 canonical codes, one doc per code, growable.

This folder is the **canonical source** of failure-code definitions. The summary in [`../conduct/failure-modes.md`](../conduct/failure-modes.md) is the at-a-glance table; the per-code docs here are where the *signature*, *counter*, and *examples* live in detail. If they conflict, this folder wins.

## Why one doc per code

Free-text failure logs don't compound. A taxonomy with named codes does — but only if every code has a precise signature and a testable counter. One doc per code means:

1. New codes can be PR'd without merge conflicts.
2. Each code has room for examples, debate, and history.
3. The boundary between adjacent codes (F04 task-drift vs. F07 over-helpful substitution) gets argued in writing, not in someone's head.

## Index

### Generation failures

- [F01 — Sycophancy](./f01-sycophancy.md)
- [F02 — Fabrication](./f02-fabrication.md)
- [F03 — Context decay](./f03-context-decay.md)
- [F04 — Task drift](./f04-task-drift.md)
- [F05 — Instruction attenuation](./f05-instruction-attenuation.md)

### Action failures

- [F06 — Premature action](./f06-premature-action.md)
- [F07 — Over-helpful substitution](./f07-over-helpful-substitution.md)
- [F08 — Tool mis-invocation](./f08-tool-mis-invocation.md)
- [F09 — Parallel race](./f09-parallel-race.md)
- [F10 — Destructive without confirmation](./f10-destructive-without-confirmation.md)

### Reasoning failures

- [F11 — Reward hacking](./f11-reward-hacking.md)
- [F12 — Degeneration loop](./f12-degeneration-loop.md)
- [F13 — Distractor pollution](./f13-distractor-pollution.md)
- [F14 — Version drift](./f14-version-drift.md)

## Per-doc shape

Every code's doc has these sections, in this order:

1. **Signature** — the precise observable pattern.
2. **Counter** — the rule that prevents recurrence.
3. **Examples** — at least two, ideally three, drawn from real observations.
4. **Adjacent codes** — what this code is *not* (the closest neighbors and how to disambiguate).
5. **Escalation** — what happens on a single occurrence vs. 3+ in one workflow.

## How to extend

Propose `F15+` only when you've observed the pattern in at least three independent contexts. PR template:

- Signature, counter, examples, adjacent codes, escalation — all six sections filled.
- The pattern does not overlap an existing code (or, if it does, propose a merger or refinement).
- The counter is testable — a reviewer can check whether the counter was applied.

Vibes-based codes get rejected. So do codes whose counter is "be more careful."

## How to read

Use this folder when:

- Tagging a failure log entry — pick the dominant code, link the doc.
- Designing a guard — read the counter, implement it.
- Onboarding a new agent / contributor to the project — point them at the index.
