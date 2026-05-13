# Metacognition — Periodic Goal-Restate Protocol

Audience: any agent on a multi-step task that spans more than a handful of tool-uses. This module is a *positive practice*, not a failure-mode counter. Where [`./doubt-engine.md`](./doubt-engine.md) fires on **decision points** (agreement, verdict, scope acceptance), this module fires **periodically on the running task itself** — a heartbeat that asks *am I still working on what the user actually asked for?*

Why now: the periodic restate catches the silent drift that no single decision-point check will catch. Each individual sub-step looked locally reasonable, yet by step 12 the agent is solving a different problem than the one stated in turn 1. A heartbeat surfaces the drift while it is still cheap to correct.

## First law

**The restate is about the *original ask*, not the *current task*.** The current task is whatever the agent is doing right now — fixing a lint error, drafting a JSON file, refactoring a helper. The original ask is what the human said in the opening turn. The restate compares the two. Drift is the signal.

## The restate sentence

One sentence, fixed shape:

> *I am trying to **\<verb\>** **\<object\>** so that **\<reason\>**.*

Three slots, all mandatory:

- **verb** — the action the user actually asked for (ship, draft, diagnose, migrate, refactor, answer).
- **object** — the thing the action operates on (this PR, the F22 module, the convergence loop, the user's question).
- **reason** — the *user's* downstream goal, not the agent's interpretation of it.

If any slot is fuzzy, the restate has failed and the agent must surface — not push on.

## Periodicity

Fire the restate every **K = 8 tool-uses** on a continuous task. Eight is a working default: long enough that the heartbeat is not noise, short enough that drift is still recoverable. Plugins MAY tune K in their local CLAUDE.md; they MUST NOT raise it past 16 without an explicit cost-of-drift argument.

The count resets when:

- The user takes a turn (their input is itself a stronger restate).\
- A subagent dispatch boundary is crossed (the dispatcher restates as part of the brief; the subagent restates on receipt).
- The agent declares a verdict and hands back.

## Off-schedule triggers

Fire immediately — do not wait for K — when any of:

1. The user asks a meta-question: *"what are you doing?"*, *"what's the goal here?"*, *"why are you doing X?"*. The question is itself the signal that the heartbeat already lapsed.
2. A dispatch boundary is crossed (orchestrator → subagent, or subagent return).
3. Two or more iterations on the same artifact have returned INCONCLUSIVE / BLOCKED / partial-failure. Cross-ref [[sunk-cost-iteration]] (F23): if the third iteration's restated goal still names the same micro-objective, fire F23's surface-to-principal check before dispatching v(N+1).
4. The agent notices it has switched primary tools (e.g., from Read/Edit to Bash + network) — tool-class transitions are common drift markers.
5. A turn elapses with no progress visible against the original criterion.

## Drift detection

After the restate, compare against the previous restate (or, on first fire, against the opening user turn):

| Comparison | Verdict | Action |
|---|---|---|
| Same verb, same object, same reason | Aligned | Continue. |
| Same verb + object, reason narrowed sensibly | Aligned | Continue; note the narrowing in the next handback. |
| Object changed (now operating on a different artifact) | Drift | Surface the shift to the user in one line *before* the next tool-use. |
| Verb changed (diagnosing instead of fixing, exploring instead of shipping) | Drift | Same — surface before continuing. |
| Reason no longer matches the user's downstream goal | Drift + likely F23 | Stop, surface, ask whether the approach is still the right shape. |

Drift is not automatically wrong — sometimes the agent has correctly discovered that the original framing was incomplete. The rule is *surface, don't silently pivot*.

## What a good restate looks like

Good:

> *I am trying to ship the F22 capability-fidelity module so that future sessions stop silently substituting when a named tool is missing.*

Bad (task-restate, not ask-restate):

> *I am trying to fix the JSON parse error in n2-output.json.*

The second sentence describes the current micro-step. It is not a restate; it is a status line. A restate that drifts into status is the most common failure of this protocol.

## Anti-patterns

- **Description-without-direction.** *"I am working on the convergence loop."* No verb, no reason, no comparison surface. Reject and rewrite.
- **Restating the *task* instead of the *original ask*.** Status of the current sub-step is not a restate. The protocol exists precisely to lift attention back to the ask.
- **Theatrical restate.** Firing the sentence every K turns with no comparison against the prior restate. The compare step is the work; the sentence is the scaffolding.
- **Restate-then-ignore.** Detecting drift, naming it internally, and pushing on anyway. The protocol's whole value is the *surface*; suppressing the finding is the failure this module exists to prevent.
- **Inflating K to dodge the heartbeat.** If the agent finds itself pushing K higher to avoid restating, the underlying issue is task length, not periodicity — break the task up instead.
- **Restate as filler.** Emitting the sentence to the user as a progress update when nothing has changed. The restate is for the agent's own attention budget; surface it only when it produced a finding.

## Relationship to other modules

| Module | Role |
|---|---|
| [`./doubt-engine.md`](./doubt-engine.md) | Decision-point check on agreement / verdict / scope acceptance |
| [`./discipline.md`](./discipline.md) § Goal-driven execution | Sets the success criterion *at the start*; this module re-checks against it *during* |
| [`./context.md`](./context.md) | Attention-budget hygiene; the restate is a top-200-tokens refresh under load |
| [[sunk-cost-iteration]] (F23) | The failure surfaced when two+ iterations return drifted restates on the same artifact |
| **`metacognition.md`** (this) | Periodic heartbeat on the running task |

A skill running the full stack: sets the goal up front (discipline § goal-driven) → fires doubt at each decision point → runs the metacognition heartbeat between decision points → surfaces drift before it compounds → escalates to F23 when two restates on the same iteration loop confirm the approach is stuck.

## Logging

When a restate catches drift:

- One-line surface in the agent's next reply, prefixed with the drift class (object-shift / verb-shift / reason-shift).
- If the drift is recurrent across the session, log to the project's precedent log under tag `metacognition-drift`.
- If the drift correlates with a stuck iteration, that's [[sunk-cost-iteration]] territory — emit per F23's contract, not this module's.

Untracked drift catches teach nothing. Logged ones compound into a sharper sense of when a task is wandering before the human has to point it out.
