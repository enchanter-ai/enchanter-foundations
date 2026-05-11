# Clause 6 — Planning

**ISO/IEC 42001:2023 §6**
**Status:** Self-attestation, **fully in scope**.
**Last reviewed:** 2026-05-05

## §6.1 Actions to address risks and opportunities

### §6.1.1 General

#### Requirement

When planning the AIMS, the organization shall consider issues from §4.1, requirements from §4.2, and determine risks and opportunities that need to be addressed to ensure the AIMS can achieve its intended outcomes, prevent or reduce undesired effects, and achieve continual improvement.

#### Our position

Risk identification + analysis + treatment is the project's strongest documented capability area. Sources:

| Source | What it provides |
|---|---|
| `wixie/security-closure/` audit | 30 documented findings F-001..F-030, Opus 4.7 + GPT 5.5 Pro synthesis |
| `wixie/inference-engine/` SPRT-elevated patterns | Cross-session recurring failures |
| `shared/conduct/precedent.md` | Per-project self-observed failures |
| `shared/conduct/failure-modes.md` | 14-code taxonomy F01-F14 |
| Per-plugin `learnings.md` | Per-iteration hypothesis-outcome log |
| This readiness package's `risk-register.md` | Consolidated AIMS-level risk register |

#### Evidence

- `wixie/prompts/security-closure/results/synthesis.md`
- `risk-register.md` (this readiness package)
- `shared/conduct/failure-modes.md`

---

### §6.1.2 AI risk assessment

#### Requirement

The organization shall define and apply an AI risk assessment process that:

- establishes and maintains AI risk criteria;
- ensures repeated assessments produce consistent, valid, comparable results;
- identifies AI risks;
- analyses AI risks;
- evaluates AI risks against the established criteria.

#### Risk criteria

Per `aims-policy.md` §4:

- Severity classes: Critical, High, Medium, Low.
- Blast-radius classes: Session, Skill, Plugin, Repo, Cross-repo, Cross-tenant.
- Hard stops: RCE, cross-tenant leak, EU CRA / EU AI Act / FedRAMP AI / SOC 2 procurement-blocker, any Critical with documented exploit path.

#### Risk identification methods

| Method | Frequency | Output |
|---|---|---|
| `wixie/deep-research` (E0) | Per claim | `claims.json`, `sources.jsonl`, `trace.json` |
| `wixie/prompt-harden` 12-attack audit | Per prompt | `audit.json` |
| Security-closure audit (Opus + GPT synthesis) | Annual (or on material change) | F-001..F-030 |
| Inference-engine substrate | Continuous | SPRT-elevated patterns |
| Precedent log | Continuous | `state/precedent-log.md` |

#### Risk analysis methods

| Method | Where applied |
|---|---|
| 5-axis Gauss convergence (clarity, specificity, robustness, format, safety) | `wixie/convergence-engine` |
| Wald SPRT (LLR thresholds: elevate ≥ 2.89, retire ≤ -2.25) | `wixie/inference-engine` |
| Beta-Binomial posteriors | `wixie/inference-engine` |
| Exponential Moving Average decay (half-life) | `wixie/inference-engine` |
| Manual severity rating in `risk-register.md` | This readiness package |

#### Risk evaluation

For each risk:

1. Severity assigned per `aims-policy.md` §4.1.
2. Blast radius assigned per `aims-policy.md` §4.2.
3. Treatment decision per `aims-policy.md` §4.3.
4. Residual risk recorded.
5. Owner + review date assigned.

#### Repeatability

- Quantitative methods (SPRT, Beta-Binomial) are deterministic given the input stream.
- Qualitative ratings (severity, blast radius) use the rubric in `aims-policy.md` §4 to reduce reviewer drift.
- Reviewer tier (Haiku) double-checks scoring with no-regression contract.

#### Evidence

- `risk-register.md`
- `wixie/prompts/security-closure/results/synthesis.md`
- `wixie/plugins/inference-engine/state/catalog.json`

---

### §6.1.3 AI risk treatment

#### Requirement

The organization shall define and apply an AI risk treatment process to select appropriate risk treatment options and determine all controls necessary to implement the chosen options.

#### Treatment options

Per `aims-policy.md` §4.3:

- Mitigate, Accept, Transfer, Avoid.

#### Active treatment queues

From `wixie/prompts/security-closure/results/synthesis.md`:

| Queue | Effort | Status |
|---|---|---|
| MUST-SHIP | ~120h | Active (Sprint 1-2) |
| HIGH-CONFIDENCE | ~140h | Queued (Sprint 3) |
| DEFERRED | ~120h | Scheduled (Sprint 4 + later) |

#### MUST-SHIP items

| F | Risk | Treatment | Target |
|---|---|---|---|
| F-001 | SBOM emission default-off | Implement shared `release.yml` w/ SBOM | Q2 2026 |
| F-002 | Signed provenance missing | Sigstore + SLSA L3 | Q2 2026 |
| F-004 | Prompt-injection canaries not CI-blocking | Promote `hydra/canary` to CI gate | Q2 2026 |
| F-005 | Egress allowlist observe-only | Promote `hydra/egress-monitor` to policy | Q2-Q3 2026 |
| F-010 | Runtime capability sandbox missing | Per-subagent sandbox (critical RCE primitive) | Q2 2026 |
| F-013 | Per-tenant rate limiting | Hydra rate-limit harness | Q3 2026 |

#### Annex A reference controls statement

ISO 42001 §6.1.3 d) requires comparing necessary controls with Annex A reference controls. Mapping done in `../annex-a-controls/` directory (this readiness package).

#### Statement of applicability (SoA)

Not formally required by ISO 42001 (unlike ISO 27001), but produced as a courtesy in `../annex-a-controls/SoA.md`. Each Annex A control: applicable / not-applicable + justification + evidence.

#### Evidence

- `wixie/prompts/security-closure/results/synthesis.md`
- `risk-register.md`
- `../annex-a-controls/` (this readiness package)

#### Gap

- MUST-SHIP queue not closed. Q2-Q3 2026 target. Tracked in `risk-register.md` per F-code.

---

## §6.2 AI objectives and planning to achieve them

### Requirement

The organization shall establish AI objectives at relevant functions and levels. Objectives shall be:

- consistent with the AI policy;
- measurable (if practicable);
- take into account applicable requirements;
- relevant to conformity of AI systems;
- monitored;
- communicated;
- updated as appropriate.

### Our objectives

| Objective | Measurement | Target | Communication |
|---|---|---|---|
| Every shipped prompt meets DEPLOY bar | σ<0.45, overall≥9.0, all axes≥7.0, 8/8 SAT | 100% | `wixie/CLAUDE.md` |
| MUST-SHIP queue closed | F-001, F-002, F-004, F-005, F-010, F-013 status | All shipped by end Q3 2026 | `synthesis.md` + `risk-register.md` |
| No-regression on convergence axes | Auto-revert on regression | Enforced by convergence engine | `wixie/CLAUDE.md` |
| Audit-trail HMAC chain integrity | Periodic verification | 100% chain intact | `hydra/audit-trail` runbook |
| Inference-engine reconcile cadence | Weekly + pre-high-stakes | 100% briefings fresh | `shared/conduct/inference-substrate.md` |
| Self-attestation freshness | Quarterly | Re-attested every 90d | Compliance maps |
| Conduct-module conformance | Per-skill SKILL.md frontmatter | 100% conformant | `shared/conduct/skill-authoring.md` |

### Planning to achieve them

- Sprint-level breakdown in `wixie/prompts/security-closure/results/synthesis.md`.
- Per-plugin `learnings.md` records iteration plans.
- Per-prompt convergence loop has explicit success criterion.

### Evidence

- `wixie/CLAUDE.md` § DEPLOY bar
- `wixie/prompts/security-closure/results/synthesis.md`
- Per-prompt `metadata.json` files

### Gap

- No automated dashboard aggregating objectives status. Operator-private dashboards exist; not standardized. Tracked R-009.

---

## §6.3 Planning of changes

### Requirement

When the organization determines the need for changes to the AIMS, the changes shall be carried out in a planned manner.

### Our change-management process

1. **Proposed change**: PR or issue against the relevant repo.
2. **Impact assessment**: against AIMS scope (§4.3), risk register, conduct modules.
3. **Reviewer-tier check** (Haiku): does the change conform to existing conduct modules?
4. **Convergence check** (Sonnet): does the change pass the no-regression contract on relevant axes?
5. **Owner approval** (AI Owner / Custodian per scope).
6. **Merged**: update conduct module / SKILL.md / policy as needed.
7. **Logged**: change recorded in plugin's `learnings.md` and (if material) in inference-engine substrate.

### Material vs. routine changes

| Material (requires AI Owner approval) | Routine (Custodian-level) |
|---|---|
| New plugin family | Bug fix in existing skill |
| Change to AIMS scope | Documentation update |
| Change to conduct module | Test addition |
| Change to AI principle | Refactor without behavior change |
| New cert-body engagement | Per-prompt iteration |
| Change to risk acceptance criteria | New `learnings.md` entry |

### No-regression contract

`wixie/convergence-engine` auto-reverts an iteration that regresses on a tested axis. The hypothesis is logged with F12 (degeneration loop), and a different axis is selected for the next round.

### Evidence

- Git history across repos
- Per-plugin `learnings.md`
- `wixie/CLAUDE.md` § DEPLOY bar (no-regression contract)

### Gap

- Change-management process is mostly tribal/conduct-encoded; no formal change advisory board. Acceptable for current scale.
