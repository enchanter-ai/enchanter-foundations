# Clause 10 — Improvement

**ISO/IEC 42001:2023 §10**
**Status:** Self-attestation, **fully in scope**.
**Last reviewed:** 2026-05-05

## §10.1 Nonconformity and corrective action

### Requirement

When a nonconformity occurs, the organization shall:

- react to the nonconformity, taking action to control and correct it, and dealing with consequences;
- evaluate the need for action to eliminate the cause(s);
- implement any action needed;
- review effectiveness of any corrective action taken;
- update risks and opportunities;
- make changes to the AIMS, if necessary.

The organization shall retain documented information of nonconformity, action taken, and results.

### Our nonconformity handling

| Stage | Mechanism |
|---|---|
| Detection | F-code logging (`shared/conduct/failure-modes.md`); reviewer-tier reject; convergence regression; audit-trail anomaly; precedent-log entry |
| React | Auto-revert on regression (no-regression contract); manual revert otherwise; isolate plugin if scoped |
| Evaluate cause | F-code taxonomy provides causal categories; `learnings.md` records hypothesis-outcome |
| Implement action | Counter from `shared/conduct/failure-modes.md`; precedent-log entry with signal |
| Review effectiveness | Next iteration of convergence loop; SPRT elevation if pattern persists |
| Update risks | `risk-register.md` updated as needed |
| Update AIMS | Conduct module update on recurring pattern; policy update on material |

### Documented information

| Artifact | Records |
|---|---|
| Per-prompt `learnings.md` | Per-iteration hypothesis + outcome + F-code |
| `state/precedent-log.md` | Self-observed operational failures + counters |
| `inference-engine/state/artifacts.jsonl` | Cross-session emitted patterns |
| `inference-engine/state/catalog.json` | SPRT-reconciled posteriors + verdicts |
| `risk-register.md` | AIMS-level risks + treatments |
| Audit-trail `log.jsonl` | Real-time event log |

### Escalation patterns (per failure-modes.md)

| Code | Single occurrence | 3+ in one prompt |
|---|---|---|
| F01, F02, F07, F13 | Log and continue | Escalate — systemic issue |
| F03, F04, F05 | Checkpoint + reset context | Re-scope the task |
| F06, F08, F09, F10 | Revert, log, retry | Pause plugin — contract broken |
| F11, F12 | Revert, switch axis | Freeze convergence on this prompt |
| F14 | Regenerate against current registry | Audit the registry freshness |

### Evidence

- `shared/conduct/failure-modes.md`
- `shared/conduct/precedent.md`
- Per-plugin `learnings.md`
- `wixie/plugins/inference-engine/`

### Gap

None at clause level.

---

## §10.2 Continual improvement

### Requirement

The organization shall continually improve the suitability, adequacy, and effectiveness of the AIMS.

### Our continual-improvement engine

The **inference-engine substrate** is purpose-built for §10.2 compliance.

| Component | Function |
|---|---|
| `artifacts.jsonl` | Append-only log of cross-session-relevant failures + counters |
| `inference-engine.py reconcile` | Wald SPRT + Beta-Binomial reconciliation → updates `catalog.json` |
| `state/briefings/<plugin>.md` | Per-plugin top-of-context briefings consumed at session start |
| Pattern lifecycle | Emitted → reconciled → elevated (LLR ≥ 2.89) → consumed → retired (LLR ≤ -2.25) |

### Improvement cadence

| Trigger | Cadence |
|---|---|
| Emit | On any cross-session-relevant failure with named counter |
| Reconcile | After emit burst (>1 in session); pre-high-stakes; weekly cron |
| Briefing read | Session start by target plugin's primary skill |
| Conduct module update | When 3+ similar SPRT-elevated patterns warrant new F-code or counter clarification |
| Policy update | Annual or on material change |

### Recursion bound

Per `shared/conduct/inference-substrate.md`:

- Depth-1: substrate watches itself via `substrate-failure` category artifacts.
- Depth-2: no — depth-2 escalates to human via `inference.escape-valve` file touch.

### Retirement

- LLR < -2.25 over multiple reconciles → pattern marked `retired`.
- Retired patterns don't appear in briefings but stay in `catalog.json` for history.
- Re-emit retired pattern with same fingerprint is rejected; if pattern genuinely recurs, emit with a narrower or reframed `code` (e.g., F07.1).

### Evidence

- `shared/conduct/inference-substrate.md`
- `wixie/plugins/inference-engine/state/`
- `wixie/plugins/inference-engine/SKILL.md`

### Gap

- Opt-in gate (`WIXIE_INFERENCE_ENABLED=1`) — substrate is rollout-flagged. Pre-Phase-1-backfill validation pending on clean machine. Tracked R-010.
- No automated F-code-vs-substrate cross-validation. Acceptable for current scale.

---

## Closing note for clause 10

The combination of:

- F-code taxonomy (14 codes; deliberate growth)
- Per-workflow `learnings.md` (immediate iteration log)
- Project-level `precedent-log.md` (durable operational gotchas)
- Inference-engine substrate (cross-session SPRT-elevated patterns)
- Quarterly self-re-attestation (compliance maps refresh)
- Annual security-closure audit (cross-vendor synthesis)

...constitutes a layered continual-improvement system whose primitives are:

1. **Detection** — automatic (convergence + reviewer) + advisory (audit-trail + naga) + manual (precedent log).
2. **Causal analysis** — F-code taxonomy.
3. **Counter application** — `failure-modes.md` per-code counter.
4. **Cross-session compounding** — inference-engine SPRT elevation.
5. **Top-of-context delivery** — briefings at session start.

This is the strongest area of the AIMS in evidence terms. Cert-body auditors should find clause 10 well-evidenced.
