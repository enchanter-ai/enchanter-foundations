# Clause 9 — Performance evaluation

**ISO/IEC 42001:2023 §9**
**Status:** Self-attestation, **fully in scope** with §9.3 gap (management review formalism in roadmap).
**Last reviewed:** 2026-05-05

## §9.1 Monitoring, measurement, analysis, and evaluation

### §9.1.1 General

#### Requirement

The organization shall determine:

- what needs to be monitored and measured;
- methods for monitoring, measurement, analysis, evaluation, ensuring valid results;
- when monitoring and measuring shall be performed;
- when results shall be analyzed and evaluated.

#### Monitoring surfaces

| Surface | What it captures | Cadence |
|---|---|---|
| `hydra/plugins/audit-trail/state/log.jsonl` | Every tool, hook, policy decision (HMAC-chained) | Real-time |
| `wixie/plugins/inference-engine/state/artifacts.jsonl` | Cross-session emitted patterns | On emit |
| `wixie/plugins/inference-engine/state/catalog.json` | SPRT-reconciled posteriors, LLR, verdicts | On reconcile |
| `wixie/plugins/inference-engine/state/briefings/<plugin>.md` | Per-plugin briefings (top-of-context next session) | Pre-session |
| Per-prompt `learnings.md` | Hypothesis-outcome log | Per iteration |
| Per-project `state/precedent-log.md` | Operational gotchas | Per failure |
| Per-prompt `metadata.json` | DEPLOY-bar score history | Per round |
| `naga/naga-observe` drift events | Cross-session drift | Per detected drift |

#### Methods

- **Wald Sequential Probability Ratio Test (SPRT):** elevation threshold LLR ≥ 2.89; retirement threshold LLR ≤ -2.25.
- **Beta-Binomial posteriors** over success/failure counts.
- **Exponential Moving Average decay** (half-life).
- **HMAC chain** for audit log tamper-evidence.
- **SHA-1 fingerprinting** of inference-engine artifacts for dedup + integrity.

#### Validity assurance

- Reconcile is idempotent on identical streams.
- HMAC verification detects log tampering.
- Reviewer-tier (Haiku) double-checks scoring with no-regression contract.
- Manual audit (this readiness package) cross-checks plugin-level evidence.

#### Evidence

- `hydra/plugins/audit-trail/state/log.jsonl`
- `wixie/plugins/inference-engine/state/`
- `shared/conduct/inference-substrate.md`

---

### §9.1.2 Analysis and evaluation

#### Requirement

The organization shall evaluate the AI performance and the effectiveness of the AIMS.

#### Evaluation methods

| What | How |
|---|---|
| Per-prompt performance | DEPLOY-bar self-eval (σ, overall, axes, SAT) |
| Cross-session pattern significance | SPRT log-likelihood ratio + Beta-Binomial bounds |
| Audit-log integrity | HMAC verification on chain |
| AIMS effectiveness | This readiness package + quarterly re-attestation |
| Security posture | Security-closure audit (annual) |

#### Honest-numbers contract

Per `wixie/CLAUDE.md`:

- Stale verdicts: re-run self-eval if unsure about metadata freshness.
- 7/8 SAT pass → HOLD verdict, not DEPLOY (no inflation).
- Auto-revert on regression; log F12 (degeneration loop); pick a different axis.

#### Evidence

- Per-prompt `metadata.json`
- `wixie/plugins/inference-engine/state/catalog.json`
- This readiness package

---

## §9.2 Internal audit

### Requirement

The organization shall conduct internal audits at planned intervals to provide information on whether the AIMS:

- conforms to the organization's own requirements and to ISO 42001;
- is effectively implemented and maintained.

### Audit program

| Audit | Cadence | Auditor | Scope | Output |
|---|---|---|---|---|
| Per-prompt review | Per iteration | Reviewer-tier (Haiku) | One prompt | Score + flags |
| Inference-engine reconcile | Weekly + pre-high-stakes | Engine (automated) | Cross-session patterns | Updated `catalog.json`, briefings |
| Internal compliance audit | Quarterly | AI Auditor (Haiku-tier or human) | This entire AIMS | Updated compliance maps + risk register |
| Security-closure audit | Annual | Opus 4.7 + GPT 5.5 Pro (cross-vendor synthesis) | Full repo set | `synthesis.md` |
| Pre-cert-body dry-run | On engagement | Internal | Full readiness package | Gap report |

### Internal-audit checklist

See `../internal-audit-checklist.md` for the per-clause checklist used at quarterly cadence.

### Audit independence

- AI Auditor role separated from AI Owner (per `aims-policy.md` §5.3): the same human may not be both Owner and Auditor for the same artifact.
- Cross-vendor synthesis (Opus + GPT) in security audits provides independence at the model level.

### Evidence

- `../internal-audit-checklist.md`
- `wixie/prompts/security-closure/results/synthesis.md`
- This readiness package

### Gap

- First quarterly internal audit using this readiness package's checklist not yet exercised. Target: 2026-08-31. R-001.

---

## §9.3 Management review

### Requirement

Top management shall review the organization's AIMS at planned intervals to ensure its continuing suitability, adequacy, and effectiveness.

The review shall include consideration of:

- status of actions from previous reviews;
- changes in external/internal issues relevant to the AIMS;
- changes in needs/expectations of interested parties;
- AIMS performance, including trends in nonconformities, monitoring results, audit results, AI objectives fulfilment, risk-management effectiveness;
- adequacy of resources;
- opportunities for continual improvement.

### Our practice (template-ready, not yet exercised)

| Aspect | Provision |
|---|---|
| Cadence | Quarterly (template at `../management-review-template.md`) |
| Conductor | AI Owner |
| Inputs | All §9.3 a-f items per template |
| Outputs | Decisions, action items, updated risk register, signed re-attestation |
| Retention | 7-year retention per `aims-policy.md` §7.3 |

### Why not yet exercised

- Project formally adopted ISO 42001 readiness on 2026-05-05 (this package).
- First quarterly review scheduled 2026-08-31.
- Template (`../management-review-template.md`) ready and validated against §9.3 a-f.

### Evidence

- `../management-review-template.md`
- `aims-policy.md` §9 commitment statement template
- Risk register R-001 (tracking first review)

### Gap

- **§9.3 management review formalism: gap.** Template ready; first instance scheduled Q3 2026. Tracked R-001.
- This is the most prominent ISO 42001 gap. Cert body engagement should target a post-Q3-2026 audit to ensure at least one management-review record exists.
