# Runbooks — MTTR per Failure Code

Per-failure-mode operational runbooks keyed to the F-code taxonomy in `wixie/shared/conduct/failure-modes.md`. Each runbook follows a fixed shape: Signature, Detection (audit-trail / metrics / self-report signals), Triage steps, Rollback (in-flight + deployed), and Post-incident logging.

Closes audit findings F-007 (no MTTR runbooks) and F-049 (no per-failure-mode rollback documentation).

## Index

### Generation failures
- [F01.md](F01.md) — Sycophancy: agent abandons a flagged concern after social affirmation.
- [F02.md](F02.md) — Fabrication: cited API / flag / file does not exist.
- [F03.md](F03.md) — Context decay: top-of-context instruction violated at the bottom.
- [F04.md](F04.md) — Task drift: work expanded past the stated goal.
- [F05.md](F05.md) — Instruction attenuation: rule stated once, obeyed once, then forgotten.

### Action failures
- [F06.md](F06.md) — Premature action: edited before grounding (wrong file, wrong function).
- [F07.md](F07.md) — Over-helpful substitution: solved a problem the user didn't ask about.
- [F08.md](F08.md) — Tool mis-invocation: wrong tool for the job (e.g. Bash for read).
- [F09.md](F09.md) — Parallel race: two writes to the same file or branch.
- [F10.md](F10.md) — Destructive without confirmation: `rm`, `reset --hard`, `force push` without explicit yes.

### Reasoning failures
- [F11.md](F11.md) — Reward hacking: hit the metric by gaming it.
- [F12.md](F12.md) — Degeneration loop: same edit, reverted, re-applied across iterations.
- [F13.md](F13.md) — Distractor pollution: long irrelevant context bent the output.
- [F14.md](F14.md) — Version drift: used deprecated API / retired model ID / old flag.

## Authoring guide

New runbooks follow the template in `wixie/prompts/ecosystem-audit/specs/templates.md` § I. New F-codes must first land in `wixie/shared/conduct/failure-modes.md` per its § Extending the taxonomy clause; only then add a runbook here.

Improvements directory: file detector gaps, missing signals, or rollback issues under `improvements/` (created on first need).
