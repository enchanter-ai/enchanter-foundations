# Clause 8 — Operation

**ISO/IEC 42001:2023 §8**
**Status:** Self-attestation, **fully in scope**.
**Last reviewed:** 2026-05-05

## §8.1 Operational planning and control

### Requirement

The organization shall plan, implement, and control the processes needed to meet AI requirements and to implement the actions determined in §6. The organization shall:

- establish criteria for the processes;
- implement control of processes in accordance with the criteria;
- keep documented information to the extent necessary to have confidence the processes have been carried out as planned.

### The lifecycle is our operational control

Per `wixie/CLAUDE.md` § Lifecycle:

| Stage | Skill | Tier | Artifact |
|---|---|---|---|
| Research | `/deep-research` (auto-fires inside `/create`) | Opus + Sonnet + Haiku | `state/briefs/<slug>/{claims.json, sources.jsonl, trace.json}` |
| Craft | `/create` | Opus + Haiku | `prompt.*`, `metadata.json` |
| Refine | `/refine` | Opus + Haiku | `prompt.*` (v++), `metadata.json` |
| Converge | `/converge` | Sonnet + Haiku | `learnings.md`, scores updated |
| Test | `/test-prompt` | Sonnet | `tests.json`, pass/fail |
| Harden | `/harden` | Sonnet red-team | `audit.json` (12 attacks) |
| Translate | `/translate-prompt --to <model>` | Sonnet | `prompt.<new>`, score comparison |

Each stage is a skill with explicit preconditions, inputs, steps, outputs, and handoff (per `shared/conduct/skill-authoring.md`).

### Criteria for the processes

- DEPLOY bar: σ < 0.45, overall ≥ 9.0, all 5 axes ≥ 7.0, 8/8 SAT assertions pass.
- Reviewer-tier independent check before shipping.
- No-regression contract auto-reverts regressing iterations.
- Tier-appropriate verbosity per `shared/conduct/tier-sizing.md`.

### Documented information

Per-prompt folder:

```
prompts/<name>/
├── prompt.<ext>       production prompt
├── metadata.json      model, tokens, cost, 5-axis scores, 8 assertions, version
├── tests.json         regression test cases (≥3, ≥1 edge-case)
├── report.pdf         dark-themed audit (final)
└── learnings.md       hypothesis/outcome log
```

### Evidence

- `wixie/CLAUDE.md` § Lifecycle
- Per-prompt folders under `wixie/prompts/`
- `shared/conduct/skill-authoring.md`

### Gap

None at clause level. Per-stage gaps tracked in `risk-register.md` (e.g., R-007 for image-prompt impact-assessment gap).

---

## §8.2 AI risk assessment

### Requirement

The organization shall perform AI risk assessments at planned intervals and when significant changes are proposed or occur, retaining documented information of the results.

### Our practice

| Trigger | Assessment | Output |
|---|---|---|
| Per prompt | `/harden` 12-attack red-team | `audit.json` |
| Per prompt | 5-axis Gauss convergence | `metadata.json` |
| Cross-session | Inference-engine SPRT reconcile | `catalog.json` |
| Annual | Security-closure audit (Opus + GPT synthesis) | `synthesis.md` |
| On change | Convergence loop with no-regression | Updated `learnings.md` |

### Significant change triggers

| Trigger | Required assessment |
|---|---|
| New prompt | Full lifecycle (research → harden) |
| Material refinement to existing prompt | `/refine` + `/converge` + `/harden` |
| Cross-target deployment | `/translate-prompt` (includes score comparison) |
| Conduct module change | PR review + downstream-impact assessment |
| New plugin family | AIMS scope review (§4.3) + risk register update |

### Evidence

- Per-prompt `metadata.json`, `audit.json`
- `wixie/plugins/inference-engine/state/catalog.json`
- `wixie/prompts/security-closure/results/synthesis.md`

### Gap

- Image-prompt 12-attack coverage thinner than text-prompt coverage. Tracked R-008.

---

## §8.3 AI risk treatment

### Requirement

The organization shall implement the AI risk treatment plan and retain documented information of the results.

### Implementation status

| Queue | Status | Items shipped | Items remaining |
|---|---|---|---|
| MUST-SHIP | Active | 0 of 6 fully shipped | F-001, F-002, F-004, F-005, F-010, F-013 |
| HIGH-CONFIDENCE | Queued | Several partial (F-003, F-007, F-009, F-014, F-019, F-020) | OTLP exporter, model-watch, pager, typosquat seed refresh |
| DEFERRED | Scheduled | — | F-008, F-012, F-015, F-016, F-022 |

### Already-shipped controls

Per `wixie/prompts/security-closure/results/synthesis.md`:

- HMAC chain (audit-trail)
- F01-F21 runbooks
- Dependabot config
- license-gate
- sbom-emitter (partial — default-off)
- egress-monitor (observe-only)
- canary (advisory-only)
- capability-fence (partial)
- `<untrusted_source>` wrapping (deep-research)
- Locked appends (inference-engine)

### Evidence

- `wixie/prompts/security-closure/results/synthesis.md`
- `risk-register.md`
- Per-plugin SKILL.md + state/

### Gap

- 0 of 6 MUST-SHIP items fully closed at time of attestation. Targets per `risk-register.md`.

---

## §8.4 AI system impact assessment

### Requirement

The organization shall conduct an impact assessment for AI systems within scope of the AIMS, considering:

- intended use and reasonably foreseeable misuse;
- positive and negative impacts on individuals, groups, society;
- complexity, autonomy, criticality of the AI system;
- data quality, security, privacy;
- relevant interested parties;
- relevant requirements (regulatory, contractual, ethical).

### Our practice

| Pathway | Impact-assessment mechanism |
|---|---|
| Text-prompt lifecycle | `/harden` 12-attack audit covers misuse + adversarial + bias |
| High-stakes runtime actions | `crow/decision-gate` human-in-loop on flagged events |
| Destructive operations | `hydra/action-guard` dry-run + confirmation per `shared/conduct/verification.md` |
| Deep-research outputs | `<untrusted_source>` wrapping prevents prompt-injection escalation |
| Cross-session patterns | Inference-engine substrate accumulates evidence; high-LLR patterns elevate to briefings |

### Impact dimensions covered

| Dimension | Coverage |
|---|---|
| Intended use | SKILL.md description field; "use when" clause |
| Foreseeable misuse | `/harden` 12-attack red-team |
| Individual impact | Bias / fairness axis in scoring rubric (when applicable) |
| Societal impact | Conduct modules + AI principles in `aims-policy.md` |
| Complexity | Tier-sizing scales prompt verbosity to model capability |
| Autonomy | Subagent contracts in `shared/conduct/delegation.md` |
| Criticality | Severity classes in `aims-policy.md` §4.1 |
| Data quality | Cite hygiene in `shared/conduct/web-fetch.md` |
| Privacy | Egress monitor + redaction in audit-trail |
| Regulatory | Cross-references to NIST AI RMF, EU AI Act, FedRAMP AI |
| Contractual | Vendor TOS compliance (implicit) |
| Ethical | AI principles §3 of policy |

### Evidence

- `wixie/prompts/*/audit.json`
- `crow/decision-gate/`
- `hydra/action-guard/`
- `shared/conduct/delegation.md`

### Gap

- Image-prompt impact-assessment coverage uneven. R-008.
- No formal pre-deployment human-readable impact summary per prompt; the `audit.json` is the closest analogue. Acceptable for current scale.

---

## §8.5 AI lifecycle management (Annex A § A.6)

### Requirement (from Annex A reference controls)

The organization shall manage AI systems across their lifecycle: requirements, design, development, verification, deployment, operation, monitoring, decommissioning.

### Our lifecycle

| Phase | Skill / mechanism | Artifact |
|---|---|---|
| Requirements | `/deep-research` + manual goal-setting | `claims.json`, success criterion in `learnings.md` |
| Design | `/create` (technique selection by Opus) | `prompt.*` v1 |
| Development | `/refine` iterative | `prompt.*` v2..N |
| Verification | `/converge` + `/test-prompt` | `metadata.json`, `tests.json` |
| Deployment | `/translate-prompt` (cross-target) | Per-target `prompt.<ext>` |
| Operation | `/harden` adversarial + runtime guardrails | `audit.json` + audit-trail |
| Monitoring | Inference-engine + audit-trail + naga/naga-observe | Substrate artifacts + logs |
| Decommissioning | Retire pattern in inference-engine (LLR < -2.25); archive prompt folder | `catalog.json` retired patterns |

### Evidence

- Per-prompt folders
- `wixie/plugins/inference-engine/state/`
- `hydra/plugins/audit-trail/state/log.jsonl`

### Gap

- No formal decommissioning runbook beyond "retire + archive". Acceptable; tracked R-015.

---

## §8.6 Data quality and provenance (Annex A § A.7)

### Requirement

Data used in AI development and operation shall be of sufficient quality and provenance to support intended outcomes.

### Our practice

Per `shared/conduct/web-fetch.md`:

| Field | Rule |
|---|---|
| `url` | Exact URL fetched |
| `date` | Publish date detectable or `null` |
| `source_type` | One of `official`, `third-party`, `community`, `paper`, `other` |
| `quote` | Verbatim ≤200 chars; no paraphrase |

Paraphrase-as-quote → F02 (Fabrication) failure mode.

`<untrusted_source>` wrapping in `wixie/deep-research` segregates external data from instruction context.

### Evidence

- `shared/conduct/web-fetch.md`
- `shared/conduct/failure-modes.md` § F02
- `wixie/deep-research/` SKILL.md

### Gap

None at clause level. Per-fetcher gaps tracked in plugin learnings.
