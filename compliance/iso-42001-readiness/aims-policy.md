# AI Management System (AIMS) Policy

**Document ID:** AIMS-POL-001
**Version:** 1.0
**Effective date:** 2026-05-05
**Review cycle:** Annual (next review: 2027-05-05)
**Standard reference:** ISO/IEC 42001:2023 §5.1, §5.2, §5.3
**Scope of applicability:** enchanter-ai project (formerly enchanted-skills / enchanted-plugins)
**Status:** Self-attestation. No certification body has assessed this document.

---

## 1. Purpose and intent

### 1.1 What this policy is

This document is the **top-level policy of the AI Management System** (AIMS) operated by the enchanter-ai project, as required by ISO/IEC 42001:2023 §5.2. It establishes:

- The boundaries of the AIMS (what is in scope, what is not)
- The AI principles the organization commits to upholding
- Risk acceptance criteria for AI-related decisions
- Named roles and accountabilities (AI owner, AI custodian, AI auditor)
- The board-level / maintainer-level commitment statement (template — to be signed)
- The relationship between this policy and the twelve `shared/conduct/*.md` behavioral modules
- The escalation paths for nonconformity, incidents, and policy override

### 1.2 What this policy is not

This policy is **not**:

- A certificate of conformance. ISO 42001 certification is issued by accredited certification bodies (BSI, DNV, TÜV Rheinland, BSI, LRQA). This document supports a certification engagement; it does not substitute for it.
- A guarantee of AI safety or correctness. The AIMS is the *process* by which safety and correctness are pursued; the outcomes depend on operator diligence.
- A static document. It is reviewed annually and after any material change to the scope, technology stack, or organizational structure.

### 1.3 Honest framing

The enchanter-ai project is, as of the effective date, a **small-team / sole-maintainer open-source effort**. Several ISO 42001 requirements are scaled accordingly:

- "Top management" in §5.1 refers to the project maintainer(s).
- "Resources" in §7.1 are time and tool budget, not headcount.
- "Management review" in §9.3 is a documented quarterly self-review, not a board meeting.

Where ISO 42001 assumes an enterprise org chart and we operate at a different scale, we substitute the smallest defensible analogue and document the substitution. We do not claim conformance where we have only an analogue without explicit mapping.

---

## 2. Scope of the AIMS

### 2.1 In-scope systems

| System | Description | Repos / paths |
|---|---|---|
| Wixie | Prompt engineering lifecycle | `wixie/` |
| Hydra | Runtime guardrails, audit trail, capability fence | `hydra/` |
| Djinn | Skill packaging and discovery | `djinn/` |
| Sylph | Plugin lifecycle, PR automation | `sylph/` |
| Naga | Observability, drift monitoring | `naga/` |
| Crow | Decision-gate, human-in-loop | `crow/` |
| Pech | Budget tracking, cost watchdog | `pech/` |
| Lich | Cross-runtime adapter parity | `lich/` |
| Agent-foundations | Shared conduct, compliance, references | `agent-foundations/` |

### 2.2 In-scope activities

- Authoring, refining, converging, hardening, testing, and translating LLM prompts
- Operating runtime guardrails (capability checks, egress monitoring, audit trail)
- Cross-session evidence accumulation (inference-engine substrate)
- Self-evaluation against compliance frameworks (NIST AI RMF, SOC 2, ISO 42001, FedRAMP boundary)
- Distribution of skills, plugins, and conduct modules to downstream agents

### 2.3 Out-of-scope (explicitly)

| Item | Why out of scope |
|---|---|
| Third-party AI products consumed (Claude API, OpenAI API, etc.) | Governance is the vendor's; our scope is *our* agents |
| Customer agents built on top of our skills | The downstream operator's AIMS, not ours |
| Annex C / D supplier AI lifecycle management | We are a producer, not a third-party integrator |
| Model training / fine-tuning | We do not train; we orchestrate inference |
| Physical infrastructure | We operate on developer workstations + GitHub Actions; no on-prem |

### 2.4 Interested parties (per §4.2)

| Party | Interest | Mechanism we use to respect that interest |
|---|---|---|
| Developer-users (the human running Claude Code with our skills) | Reliable, predictable, transparent agent behavior | SKILL.md frontmatter, conduct modules, runbooks |
| Downstream agents (subagents we dispatch) | Clear contracts, scoped tools, bounded recursion | `shared/conduct/delegation.md` |
| Enterprise customers (procurement-driven readers of compliance docs) | Defensible artifacts for vendor risk assessment | This compliance/ folder |
| Cert bodies (future) | Auditable evidence per clause | This readiness package |
| Regulators (EU AI Act, US executive orders, etc.) | Provenance, transparency, accountability | Conduct modules + audit trail |
| Open-source community | Honest framing of limitations | Self-attestation language, gap registries |

---

## 3. AI principles

The project commits to the following AI principles. These are not aspirational — each maps to a concrete control already in place or on the roadmap.

### 3.1 Fairness

**Statement:** Agents shall not produce systematically biased outcomes based on protected characteristics, demographic categories, or arbitrary classifications not relevant to the task.

**Operational controls:**
- Cite hygiene in `shared/conduct/web-fetch.md` requires `source_type` field — preventing single-vendor bias in fetched evidence.
- Red-team coverage in `wixie/prompt-harden` includes bias / stereotype attacks.
- Reviewer prompts in `wixie/convergence-engine` include a fairness axis among the 5 scoring dimensions when the prompt touches user-facing content.

**Known gap:** No standalone bias-eval harness across the prompt portfolio. Roadmap item. Tracked in `risk-register.md` as R-014.

### 3.2 Accountability

**Statement:** Every action an agent takes shall be attributable to a named skill, a named tool, a named tier, and a session ID. Every emission to durable state shall be timestamped and fingerprinted.

**Operational controls:**
- `hydra/audit-trail` HMAC-chained log at `state/log.jsonl`.
- `wixie/inference-engine` artifact stamping (timestamp + SHA-1 fingerprint).
- Per-plugin `learnings.md` records hypothesis + outcome with date.
- Skill frontmatter mandates `name`, `description`, `model`, `tools` (`shared/conduct/skill-authoring.md`).

**Known gap:** OTLP / Sentry / Datadog span exporters not yet shipped (F-021 / F-024). Q2 2026 target.

### 3.3 Transparency

**Statement:** The agent shall surface its reasoning, its uncertainty, and its tool choices in a form a competent human reviewer can follow. Black-box outputs are an anti-pattern.

**Operational controls:**
- `shared/conduct/formatting.md` requires structured output (XML for Claude, sandwich for GPT).
- DEPLOY bar enforces honest-numbers contract: 8/8 SAT assertions before shipping a prompt.
- Reviewer tier (Haiku) independently scores the executor's output — `shared/conduct/verification.md` § Tier split.

**Known gap:** Self-attestation cannot replace third-party certification; we say so in every compliance doc.

### 3.4 Safety

**Statement:** Destructive operations require dry-run + explicit confirmation. Subagents operate under tool whitelists. Hooks are advisory, never load-bearing.

**Operational controls:**
- `shared/conduct/verification.md` § Dry-run for destructive ops.
- `shared/conduct/delegation.md` § Tool whitelisting per subagent.
- `shared/conduct/hooks.md` § Injection over denial.
- `hydra/action-guard` runtime confirmation for destructive ops.
- `crow/decision-gate` human-in-loop for high-stakes flagged actions.

**Known gap:** Runtime capability sandbox per subagent (F-010) is a critical roadmap item. Subagent escape would currently be an RCE primitive.

### 3.5 Privacy

**Statement:** The agent shall not exfiltrate, persist, or transmit user data beyond what the task explicitly requires. Egress is observed; sensitive data is redacted in logs.

**Operational controls:**
- `hydra/egress-monitor` observes outbound network calls.
- `hydra/audit-trail` redaction rules on log emission.
- Conduct module `shared/conduct/tool-use.md` prohibits absolute-path leakage in tracked files.

**Known gap:** Per-plugin network egress allowlist (F-005) is observe-only, not policy. Q2 2026 target.

### 3.6 Robustness

**Statement:** Prompts shall pass red-team attacks before deployment. Convergence shall not regress on tested axes. Adversarial inputs shall fail closed.

**Operational controls:**
- `wixie/prompt-harden` 12-attack audit.
- No-regression contract in `wixie/convergence-engine`.
- `<untrusted_source>` wrapping in `wixie/deep-research`.

**Known gap:** Indirect prompt injection canary not yet CI-blocking (F-004). Q2 2026 target.

### 3.7 Sustainability and proportionality

**Statement:** Compute and tokens are not free. Each call to a model is justified by the marginal value to the user, the task, or the durable state. Cost is a first-class signal.

**Operational controls:**
- Tier-sizing module (`shared/conduct/tier-sizing.md`): Haiku for mechanical, Sonnet for decomposed, Opus for intent.
- `pech/budget-watcher` cost telemetry.
- Cache + dedup in `shared/conduct/web-fetch.md`.

**Known gap:** No automated cost-per-deploy reporting per prompt. Optional roadmap.

---

## 4. Risk acceptance criteria

### 4.1 Risk severity classes

| Class | Definition | Acceptance |
|---|---|---|
| Critical | Direct RCE, cross-tenant data leak, EU CRA / FedRAMP procurement blocker, single-failure cascading to full system compromise | **Never accept.** MUST-SHIP queue. Block release. |
| High | Single-plugin compromise, single-tenant data leak, missing required compliance evidence, MTTR > 24h on production fault | Accept only with explicit time-boxed mitigation + sign-off in `risk-register.md` |
| Medium | Single-skill misbehavior, recoverable degraded state, missing nice-to-have compliance evidence | Accept with documented mitigation timeline |
| Low | Cosmetic, single-session, no durable impact, recovered by next reconcile | Acceptable; track in precedent log |

### 4.2 Blast radius classes

| Class | Definition |
|---|---|
| Session | One conversation; resolved by ending the session |
| Skill | One skill; resolved by skipping or reverting the skill |
| Plugin | One plugin's state; resolved by isolating the plugin |
| Repo | One repository's state; resolved by branch revert |
| Cross-repo | Multiple repositories; requires coordinated rollback |
| Cross-tenant | Other developers / operators affected; requires public advisory |

A critical-severity finding with cross-repo or cross-tenant blast radius **automatically requires public advisory** within 30 days under our self-imposed responsible-disclosure norm.

### 4.3 Risk treatment decision matrix

For each identified risk, the AI owner selects one of:

- **Mitigate** — implement a control that reduces likelihood, impact, or both. Default for everything not classified Low.
- **Accept** — document the rationale, the residual risk, the review date. Only for Low + Medium with high mitigation cost relative to impact.
- **Transfer** — push to a vendor / customer / cert body. Rare for an internal AIMS.
- **Avoid** — discontinue the activity. Used when the only mitigation is to remove the feature.

Decisions are recorded in `risk-register.md`. Acceptance decisions require a named owner and a named review date — never indefinite.

### 4.4 Hard stops

The following are non-negotiable acceptance refusals:

1. Any control whose absence directly enables RCE on the operator's workstation.
2. Any control whose absence enables cross-tenant data leak in multi-tenant deployments.
3. Any compliance gap that EU CRA, EU AI Act, FedRAMP AI, or SOC 2 explicitly require for our customer profile.
4. Any pattern flagged Critical with documented exploit path.

These cases bypass the risk register acceptance flow and enter the MUST-SHIP queue directly.

---

## 5. Roles and responsibilities

ISO 42001 §5.3 requires named roles. The enchanter-ai project, operating at small-team scale, names the following roles. A single individual may hold multiple roles; each role must be explicitly named in writing.

### 5.1 AI Owner

**Held by:** Project maintainer(s). As of 2026-05-05: Daniel Frenkel (substitute on review).

**Accountabilities:**
- Final authority on AIMS scope, principles, and acceptance decisions.
- Signature on this policy.
- Signature on quarterly management reviews.
- Approval of MUST-SHIP queue items and DEFERRED rationales.
- Public-advisory authority for cross-tenant incidents.

**Cannot be delegated:** acceptance of Critical-severity risk, override of conduct modules, retraction of public attestations.

### 5.2 AI Custodian

**Held by:** Per-plugin lead or sole maintainer. Plugin-level `plugin.json` `author` field is canonical.

**Accountabilities:**
- Day-to-day operation of the plugin's AIMS controls.
- Maintenance of plugin-level `learnings.md`, `precedent-log.md`, and inference-engine artifacts.
- First-line response to nonconformity within the plugin's scope.
- Escalation to the AI Owner when impact exceeds plugin scope.

### 5.3 AI Auditor

**Held by:** Reviewer-tier agent (Haiku, per `wixie/CLAUDE.md` § Agent tiers) for routine reviews; an external party for any future certification-body audit. The same human may not be both AI Owner and AI Auditor for the same artifact.

**Accountabilities:**
- Independent verification of artifacts before shipping (`shared/conduct/verification.md`).
- Quarterly internal audit per `internal-audit-checklist.md`.
- Annual policy review.
- Pre-cert-body audit dry-run when certification engagement is scheduled.

### 5.4 Incident Coordinator

**Held by:** AI Owner during active incident; rotates to AI Custodian for plugin-scoped events.

**Accountabilities:**
- Coordinate response during a Severity-Critical or Severity-High incident.
- Public-facing communication.
- Post-mortem authorship within 14 days.
- Feed lessons learned into `inference-engine/state/artifacts.jsonl`.

### 5.5 RACI summary

| Activity | Owner | Custodian | Auditor | Coordinator |
|---|---|---|---|---|
| Set AIMS scope | A/R | C | I | I |
| Approve a new plugin's scope | A/R | C | C | I |
| Approve a Critical-risk acceptance | A/R | I | C | I |
| Run quarterly internal audit | I | C | A/R | I |
| Day-to-day MUST-SHIP queue execution | A | R | I | I |
| Public advisory authorship | A/R | C | C | R |
| Manage active incident | A | C | C | R |

A = Accountable, R = Responsible, C = Consulted, I = Informed.

---

## 6. Relationship to conduct modules

This policy is the **top of the document tree**. Underneath it sit the twelve conduct modules in `shared/conduct/`. Conduct modules are operational specifics; this policy sets the frame they operate within.

| Conduct module | Policy linkage |
|---|---|
| `discipline.md` | §3.6 robustness; §3.4 safety (think-first stance) |
| `context.md` | §3.3 transparency; §3.7 sustainability |
| `verification.md` | §3.2 accountability; §3.6 robustness |
| `doubt-engine.md` | §3.3 transparency; §3.4 safety |
| `delegation.md` | §3.4 safety; §3.2 accountability |
| `failure-modes.md` | §3.2 accountability; §4 risk |
| `tool-use.md` | §3.4 safety; §3.7 sustainability |
| `formatting.md` | §3.3 transparency |
| `skill-authoring.md` | §3.3 transparency; §3.2 accountability |
| `hooks.md` | §3.4 safety |
| `precedent.md` | §3.2 accountability; §10 improvement linkage |
| `tier-sizing.md` | §3.7 sustainability |
| `web-fetch.md` | §3.5 privacy; §3.7 sustainability |
| `inference-substrate.md` | §10 continual improvement |

**Precedence rule:** when a conduct module conflicts with this policy, the policy wins. When a plugin-local instruction conflicts with a conduct module, the plugin wins (per `wixie/CLAUDE.md`), but the override must be logged.

**Override logging requirement:** any deviation from this policy or any conduct module shall be recorded in the relevant plugin's `learnings.md` with the F-code that applies, the rationale, and the time-box.

---

## 7. Documentation control

### 7.1 Document hierarchy

```
AIMS Policy (this document)
├── Compliance maps
│   ├── ISO 42001 clause-by-clause/ (this readiness package)
│   ├── NIST AI RMF (nist-ai-rmf.md)
│   ├── SOC 2 (soc2.md)
│   └── FedRAMP boundary (fedramp-boundary.md)
├── Conduct modules (shared/conduct/*.md)
├── Skill catalogs (per-plugin SKILL.md)
├── Operational artifacts
│   ├── learnings.md per workflow
│   ├── precedent-log.md per project
│   ├── inference-engine/state/artifacts.jsonl
│   └── audit-trail/state/log.jsonl
└── Risk register (risk-register.md)
```

### 7.2 Versioning

- This policy: semantic major.minor; major bumps on scope change, minor on principle refinement.
- Conduct modules: undated; tracked via git history.
- Risk register: living document; entries dated.
- Compliance maps: dated; quarterly re-attestation.

### 7.3 Retention

- Audit-trail logs: 24 months minimum (operator-configurable; SOC 2 minimum).
- Inference-engine artifacts: indefinite, append-only (rotation deferred).
- Learnings: indefinite.
- Management review minutes: 7 years (financial-records analogue).
- Policy versions: indefinite via git.

### 7.4 Access control

- All policy + conduct documents are public-by-default in the open-source repos.
- Private operator deployments may keep their `risk-register.md` and `learnings.md` private.
- Audit-trail logs are operator-private by default; never committed to public repos.

---

## 8. Communication

### 8.1 Internal

- Conduct modules are loaded at session start via `@shared/conduct/*.md` references in `CLAUDE.md`.
- Inference-engine briefings are read at session start by the target plugin's primary skill (top-200-tokens U-curve slot).
- Per-plugin `learnings.md` is consulted before each iteration of a convergence loop.

### 8.2 External

- Public attestation documents (this folder) on the open-source repos.
- Public advisories on Critical-severity cross-tenant findings within 30 days of confirmation.
- Quarterly self-re-attestation timestamp updated on each compliance map.

### 8.3 Channels

- Source-of-truth: `agent-foundations/compliance/` (this folder + siblings).
- Discussion: GitHub issues / PRs.
- Incident: GitHub Security Advisories.

---

## 9. Board-level / maintainer commitment statement (template)

> The undersigned, acting in the capacity of AI Owner of the enchanter-ai project, commits to:
>
> 1. Maintaining the AI Management System as documented in this policy and in the supporting compliance package at `agent-foundations/compliance/iso-42001-readiness/`.
> 2. Providing the resources (time, tooling, budget) needed to operate the AIMS at the small-team scale at which the project operates.
> 3. Reviewing this policy annually, and after any material change to scope, technology, or organizational structure.
> 4. Conducting quarterly management reviews per the template at `management-review-template.md`.
> 5. Treating the AI principles in §3 of this policy as non-negotiable defaults, with overrides documented in the manner §6 requires.
> 6. Disclosing material AIMS limitations honestly, including the gaps recorded in this readiness package.
> 7. Escalating Critical-severity findings to public advisory within 30 days of confirmation.
> 8. Refraining from claiming ISO 42001 certification without an accredited certification body's certificate.
>
> _Signature:_ ____________________________
>
> _Name:_ _________________________________
>
> _Role:_ AI Owner — enchanter-ai project
>
> _Date:_ _________________________________

This template is to be physically or digitally signed by the named AI Owner at the time of formal policy adoption. The unsigned version, as it appears in source control, is the proposed text. Signed copies are retained in operator-private storage.

---

## 10. Escalation and incident paths

### 10.1 Routine nonconformity

A nonconformity is any observed deviation from this policy, a conduct module, or a documented control. Routine path:

1. Log in the relevant plugin's `learnings.md` with the F-code.
2. Apply the counter from `shared/conduct/failure-modes.md`.
3. If the same F-code recurs 3+ times in one session, escalate to the AI Custodian.
4. If across sessions (SPRT-elevated to the inference-engine substrate), the briefing is updated automatically.

### 10.2 Severity-High incident

Examples: data loss, audit-trail tamper, repeated capability bypass, F-code recurring 5+ times in a single prompt.

1. AI Custodian notifies AI Owner within 24h.
2. AI Owner activates the Incident Coordinator role.
3. Post-mortem authored within 14 days.
4. Corrective action recorded in `risk-register.md` with target date.

### 10.3 Severity-Critical incident

Examples: confirmed RCE, cross-tenant data leak, compromised audit-trail HMAC key, supply-chain compromise on enchanter releases.

1. AI Owner activates Incident Coordinator immediately.
2. Affected releases pulled within 4 hours of confirmation.
3. Public advisory issued via GitHub Security Advisory within 72 hours.
4. Post-mortem within 14 days; full timeline within 30 days.
5. Root-cause + corrective action emitted to inference-engine substrate.

### 10.4 Whistleblower / out-of-band reporting

Any developer-user, downstream operator, or member of the public may report suspected AIMS failures via GitHub Security Advisory or via direct contact to the AI Owner. Reports are acknowledged within 7 days; substantive response within 30 days.

The project commits to not retaliating against good-faith reports, including reports that turn out to be incorrect or premature.

---

## 11. Policy review and update

### 11.1 Scheduled review

This policy is reviewed:

- Annually on the anniversary of the effective date.
- After any change to the AIMS scope (new plugin family, removed plugin, scope contraction).
- After any Severity-Critical incident.
- After any external regulatory change materially affecting our customer profile.

### 11.2 Review output

A reviewed policy emits:

- A version bump (major if scope changed, minor otherwise).
- A signed re-attestation in §9.
- An updated `risk-register.md` with the review's findings.
- A changelog entry at the bottom of this document.

### 11.3 Changelog

| Version | Date | Change | Approver |
|---|---|---|---|
| 1.0 | 2026-05-05 | Initial issue of AIMS policy for certification-readiness package | AI Owner (template) |

---

## 12. References

- ISO/IEC 42001:2023 — Information technology — Artificial intelligence — Management system
- ISO/IEC 22989:2022 — AI concepts and terminology (referenced for definitions)
- ISO/IEC 23894:2023 — AI risk management (referenced for §6 alignment)
- NIST AI Risk Management Framework 1.0 + Generative AI Profile (cross-reference: `nist-ai-rmf.md`)
- SOC 2 Trust Services Criteria (cross-reference: `soc2.md`)
- FedRAMP AI baseline (cross-reference: `fedramp-boundary.md`)
- Internal: `agent-foundations/shared/conduct/*.md`
- Internal: `wixie/CLAUDE.md`
- Internal: `wixie/prompts/security-closure/results/synthesis.md`

---

## 13. Glossary

- **AIMS** — AI Management System. The set of policies, processes, roles, and artifacts that govern AI development and operation.
- **Agent** — A skill or subagent acting under this AIMS, typically Claude operating under a tier (Opus / Sonnet / Haiku).
- **Conduct module** — A `shared/conduct/*.md` file specifying operational defaults.
- **Plugin** — A self-contained unit of capability (one of: wixie, hydra, djinn, sylph, naga, crow, pech, lich, agent-foundations).
- **Skill** — A slash-command-invoked unit of work within a plugin.
- **F-code** — A code from the 14-entry failure-mode taxonomy in `shared/conduct/failure-modes.md`.
- **DEPLOY bar** — The shipping criterion in `wixie/CLAUDE.md`: σ < 0.45, overall ≥ 9.0, all axes ≥ 7.0, 8/8 SAT assertions pass.
- **SPRT** — Wald Sequential Probability Ratio Test; used by the inference-engine substrate.
- **Substrate** — The inference-engine's append-only artifact stream + reconciled catalog.

---

*End of AIMS Policy. This document is the apex of the AIMS documentation tree.*
