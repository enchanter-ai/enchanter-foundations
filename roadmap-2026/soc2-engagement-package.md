# SOC 2 Engagement Package — Auditor Selection + Type II Observation Kickoff

Status: Operator-ready, 2026-05-05. Owner: Compliance lead. Cycle: Type I (1 month) → Type II (6 month observation + 4-6 week report).

This package assumes the shipped evidence infrastructure at `vis/compliance/soc2-evidence/` is live: AIMS policy signed, risk register approved, internal audit #1 closed, automated evidence collection on cron, dashboards reachable. If any of those four are not green, do not start engagement — fix first.

Throughout: TSC = Trust Services Criteria; CC = Common Criteria; SOC 2 Type II requires a 3-12 month observation window (industry default: 6 months for first cycle, 12 months thereafter).

---

## 1. CPA firm comparison

Pricing brackets below reflect 2025-2026 market quotes for a Series-A-stage SaaS with ~30 controls and 1 AICPA-recognized TSC scope (Security only; +20-40% per added TSC: Availability, Confidentiality, Processing Integrity, Privacy).

| Firm | URL | AI / agent-tech experience | Type I pricing | Type II pricing | Turnaround (Type II report after period end) | Automation platform fit |
|---|---|---|---|---|---|---|
| **A-LIGN** | a-lign.com | Strong — audited multiple LLM-platform vendors (publicly: Anthropic enterprise customers, several Y-Combinator AI cos.). In-house AI/ML practice since 2023. | $15-25k | $35-60k | 4-6 weeks | Native integration: Vanta, Drata, Secureframe, Tugboat Logic, Thoropass |
| **Schellman** | schellman.com | Very strong — top-tier for cloud-native + AI. Audits AWS, Anthropic-tier infra vendors. Pioneered ISO 42001 + SOC 2 combined opinions. | $20-30k | $45-75k | 5-7 weeks | Native: Vanta, Drata, Secureframe. Also accepts custom evidence APIs |
| **Prescient Assurance** | prescientassurance.com | Moderate — startup-focused, ~200 SOC 2 engagements/year. AI-tech experience growing but less depth than A-LIGN/Schellman. | $10-15k | $20-35k | 4-8 weeks | Strong Vanta/Drata partnership; bundled discounts |
| **Linford & Company** | linfordco.com | Moderate — generalist boutique, well-respected on quality. Less AI-specific work but strong on technical controls. | $15-22k | $30-50k | 6-10 weeks | Accepts platform exports; not deeply integrated |
| **Sensiba San Filippo (Sensiba LLP)** | sensiba.com | Light — primarily traditional SaaS / FinTech. AI engagements rare. | $12-20k | $25-45k | 6-8 weeks | Vanta partner; Drata accepted |
| **BARR Advisory** | barradvisory.com | Moderate-strong — cloud security focus, AICPA contributor. Growing AI practice. Known for thorough CC7 testing. | $15-25k | $35-55k | 5-7 weeks | Native: Vanta, Drata, Secureframe, Hyperproof |
| **Vanta + CPA partnership (Advantage program)** | vanta.com/audit-managed | Variable — Vanta routes to vetted CPA partners (often Prescient, Insight Assurance, Johanson Group). AI depth depends on partner draw. | Bundled $10-18k | Bundled $22-40k | 4-6 weeks | Tightest possible Vanta fit (designed-for) |

Notes:
- "AI-tech experience" weighs whether the firm understands stochastic model outputs as control evidence (e.g., LLM judge eval logs as CC7.2 monitoring artifacts). Firms without this depth force you to translate every agent-specific control into traditional language.
- Pricing scales with: # of TSCs in scope, headcount, # of in-scope systems, # of subservice organizations, complexity of access model.
- The "Vanta + CPA" model trades auditor selection control for tighter automation. Reasonable when controls are standard; risky when you need a CPA who can sign off on novel agent-tech controls.

---

## 2. Engagement letter template

Standard sections expected from any CPA firm. Negotiate the bracketed items aggressively — defaults often favor the auditor.

```
1. Parties + scope
2. Engagement type (SOC 2 Type I or Type II) — explicit
3. Trust Services Criteria in scope — list them (Security only, or +A/C/PI/P)
4. System description boundary — name systems, subservice orgs (AWS, Vercel, etc.)
5. Observation period — start date and end date (Type II only); negotiate START
6. Sampling methodology — sample sizes per population (typical: 25 for n>250, 10% for n<250)
7. Opinion delivery timing — weeks after period end; negotiate ≤ 6 weeks
8. Deliverables — final SOC 2 report, bridge letter availability, gap letter
9. Surveillance / annual renewal terms — pricing lock for year 2-3
10. Fees + payment terms — fixed vs T&M; require fixed for first cycle
11. Auditor independence representations
12. Indemnification + limitation of liability — cap at fees paid
13. Termination clauses
14. Confidentiality + data handling — auditor must agree to evidence-room scope
```

**Key clauses to negotiate:**

| Clause | Default (auditor-favorable) | Push for |
|---|---|---|
| Observation period start | "Upon engagement letter execution" | Backdate to first day evidence collection began (your `soc2-evidence/` cron start date) — saves 4-8 weeks |
| Sampling methodology | "At auditor's discretion" | Explicit table tied to AICPA AT-C §205; require population disclosure before sampling |
| Opinion delivery | "Within reasonable time" | Hard SLA: draft within 4 weeks of period end, final within 6 weeks |
| Surveillance pricing | "TBD annually" | Year 2 capped at +5% of year 1; year 3 capped at +5% of year 2 |
| Re-performance | Auditor may re-test any control at any time | Bound re-performance to material change events; otherwise once per cycle |
| Scope creep | "Additional work billed at standard rates" | Any scope change requires written change order with fixed price |
| Evidence rejection | Auditor may unilaterally reject | Disputed evidence triggers a 5-business-day meet-and-confer before rejection sticks |
| Bridge letter | Often $2-5k extra | Include 2 bridge letters per year in base fee |

---

## 3. Observation period start checklist

The observation period is the 6 months the auditor will sample evidence from. Starting it before prerequisites are green guarantees CC-level findings.

### Day 0 prerequisites (must be green before kickoff)

- [ ] **AIMS policy signed** — versioned in `vis/compliance/soc2-evidence/policies/aims-policy-v1.md`, executive signature captured, ack-form completed by all engineers.
- [ ] **Risk register approved** — `compliance/soc2-evidence/risk-register.json` reviewed in management review meeting; minutes attached.
- [ ] **Internal audit #1 complete** — `compliance/soc2-evidence/internal-audits/IA-001/` contains scope memo, findings, management responses, remediation owner + due date.
- [ ] **Evidence collection cron running** — `compliance/soc2-evidence/automation/cron-status.json` shows ≥ 7 consecutive days of green pulls (access reviews, change tickets, vuln scans, backup verifications, monitoring alerts).
- [ ] **Dashboard accessible** — auditor-readable URL or report export (`compliance/soc2-evidence/dashboard/`) with role-based access; auditor account provisioned read-only.
- [ ] **Control inventory locked** — all in-scope controls (~30-50 for Security TSC) numbered (CC1.1 through CC9.2), each with: owner, frequency, evidence type, automation status.
- [ ] **Subservice org register** — every vendor in scope (AWS, Vercel, Anthropic API, etc.) has SOC 2 report on file (in `compliance/soc2-evidence/vendor-reports/`), reviewed and date-stamped.
- [ ] **Access review #1 complete** — first quarterly access review executed, anomalies remediated, evidence stored.

If any unchecked: STOP. Fix before kickoff. A 6-month observation that starts on rotten foundation produces qualified opinion.

### Day 1-30 checkpoints

- [ ] Day 1: Auditor kickoff call. Walkthrough of `compliance/soc2-evidence/` directory layout. Auditor confirms evidence access.
- [ ] Day 7: First weekly evidence health report generated; zero gaps tolerated.
- [ ] Day 14: First management review meeting under observation period. Minutes in `compliance/soc2-evidence/management-reviews/`.
- [ ] Day 21: Auditor sends Provided-by-Client (PBC) request #1 — initial population disclosures. Respond within 5 business days.
- [ ] Day 30: First monthly control-effectiveness self-assessment. Any failed control: remediate within 48h, document remediation, evidence both the failure and the fix (do NOT hide the failure — auditors detect deletion).

### Day 90 mid-cycle review

- [ ] Run a full evidence gap analysis against the control inventory. Every control must have ≥ 90 days of consecutive evidence.
- [ ] Convene auditor for informal mid-cycle review (no extra fee if in engagement letter). Surface any control with thin evidence; agree remediation path.
- [ ] Run internal audit #2 (`compliance/soc2-evidence/internal-audits/IA-002/`).
- [ ] Review vendor risk: any new subservice org? SOC 2 reports refreshed?
- [ ] Re-run access review #2.
- [ ] Update risk register; document any new risks discovered during the period.

Day 90 is the last cheap point to fix a systemic gap. After Day 120, gaps become observations in the final report.

---

## 4. Vanta / Drata / Secureframe integration

These platforms automate ~60-80% of control monitoring. They sync with cloud accounts (AWS, GCP, Okta, GitHub, Jira, etc.), continuously test configurations against control frameworks, and produce auditor-ready evidence packages.

### Platform comparison

| Platform | URL | Annual cost (Series A scale) | Best for |
|---|---|---|---|
| **Vanta** | vanta.com | $15-25k | Broadest integration library; tightest Big-4 + boutique CPA partnerships; weakest custom-evidence story |
| **Drata** | drata.com | $14-22k | Best customization + custom-control authoring; strong policy management |
| **Secureframe** | secureframe.com | $12-20k | Strongest in healthcare-adjacent (HIPAA + SOC 2 combo); good UI; smaller integration library |

### How it syncs with `compliance/soc2-evidence/`

The shipped `soc2-evidence/` directory remains source-of-truth. Platform is a **read-and-monitor layer** over it, plus a sync source for cloud-config evidence the local cron doesn't capture.

```
compliance/soc2-evidence/
├── policies/                    ← platform mirrors as "policy library"
├── risk-register.json           ← platform imports as "risk assessment"
├── automation/cron-status.json  ← platform reads; supplements with its own probes
├── vendor-reports/              ← platform mirrors as "vendor risk module"
├── access-reviews/              ← platform may auto-generate from IdP sync
├── internal-audits/             ← platform stores audit workflow + findings
├── management-reviews/          ← platform tracks meeting cadence + minutes
└── control-inventory.json       ← platform maps to its framework template
```

Integration pattern:
1. Platform connects to AWS / Okta / GitHub / Jira / endpoint-MDM via OAuth or service account.
2. Platform runs ~200-400 automated tests every 24h.
3. Failing tests → ticket + Slack alert + dashboard red mark.
4. Auditor gets read-only access to platform; pulls evidence packages directly.
5. Our `soc2-evidence/` cron continues running as the **authoritative local copy** (defense against vendor lock-in).

### Pros

- Automated control monitoring across cloud accounts (no manual screenshots).
- Vendor risk assessment module: send security questionnaires, track SOC 2 report expirations, score residual risk.
- Pre-built control mappings to SOC 2, ISO 27001, ISO 42001, HIPAA, GDPR — reuse evidence across frameworks.
- Auditor dashboard reduces PBC back-and-forth by ~50% (faster Type II turnaround).
- Continuous monitoring → catch drift between audits.

### Cons

- **Lock-in** — exporting evidence at contract end is awkward; control mappings are platform-specific.
- **Additional config burden** — every new system needs an integration or custom-test author.
- **False sense of coverage** — platform tests are necessary, not sufficient; novel agent-tech controls (LLM eval logs, prompt-injection defense evidence) still need manual evidence in `soc2-evidence/`.
- **Cost compounds** — $15-25k/year for platform + $35-60k/year for auditor = $50-85k/year all-in for first cycle.
- **Sub-processor expansion** — the platform itself becomes a subservice org in your SOC 2 boundary; need their SOC 2 report on file.

**Recommendation:** Adopt Vanta or Drata after the first Type I, before Type II observation begins. Type I is too tight a window to benefit; Type II is where continuous monitoring pays back.

---

## 5. Auditor selection decision matrix

Weights chosen to reflect agent-tech startup priorities: AI depth and platform fit dominate because they reduce translation overhead per control.

| Criterion | Weight | Score 1-5 rubric |
|---|---|---|
| AI / agent-tech depth | 30% | 5 = audited LLM platforms; 3 = audited cloud SaaS; 1 = traditional only |
| Pricing | 25% | 5 = ≤ $25k Type II; 3 = $25-45k; 1 = > $60k |
| Automation-platform fit | 20% | 5 = native integration w/ chosen platform; 3 = accepts exports; 1 = manual only |
| Timeline (report delivery) | 15% | 5 = ≤ 4 weeks; 3 = 6 weeks; 1 = ≥ 8 weeks |
| References | 10% | 5 = 3+ comparable AI-startup references reachable; 1 = no references provided |

Scoring template (fill in after RFP):

| Firm | AI depth ×30% | Pricing ×25% | Platform ×20% | Timeline ×15% | Refs ×10% | **Weighted total** |
|---|---|---|---|---|---|---|
| A-LIGN | _ | _ | _ | _ | _ | _ |
| Schellman | _ | _ | _ | _ | _ | _ |
| Prescient Assurance | _ | _ | _ | _ | _ | _ |
| Linford & Co. | _ | _ | _ | _ | _ | _ |
| Sensiba LLP | _ | _ | _ | _ | _ | _ |
| BARR Advisory | _ | _ | _ | _ | _ | _ |
| Vanta+CPA partner | _ | _ | _ | _ | _ | _ |

Decision rule: highest weighted total wins, but **any firm scoring < 3 on AI depth is disqualified** for an agent-tech business — translation overhead will eat the cost difference.

Indicative ranking for Series-A agent-tech SaaS (subject to RFP refinement):
1. Schellman (AI depth wins; pricing premium accepted)
2. A-LIGN (close second; better automation-platform integration)
3. BARR Advisory (strong CC7; mid-tier pricing)
4. Vanta+CPA bundled (cost-optimal; AI depth varies by partner draw)

---

## 6. Common Type II failure modes to preempt

These are the recurring qualified-opinion and exception drivers in 2025-2026 SOC 2 reports. Each one is preemptable with shipped infrastructure.

| Failure mode | TSC area | Why it happens | Preemption via shipped infrastructure |
|---|---|---|---|
| Missing management reviews | CC1.4, CC1.5 | Meetings happen, minutes don't get written / signed | `compliance/soc2-evidence/management-reviews/` cron requires signed PDF every 30 days; absence triggers Slack alert |
| Evidence gaps in CC7 (system operations / monitoring) | CC7.1, CC7.2, CC7.3, CC7.4 | Alerts fire and resolve, but logs of triage decisions vanish | `soc2-evidence/automation/alert-triage-log.jsonl` captures every alert + decision + actor + timestamp; immutable append-only |
| Inadequate vendor risk | CC9.2 | Vendor SOC 2 expires mid-period, no one notices | `soc2-evidence/vendor-reports/` cron checks report expiration weekly; auto-files renewal request 60 days before expiry |
| Weak access reviews | CC6.2, CC6.3 | Quarterly review treated as checkbox; no evidence of remediation | Access review cron pulls IdP, diffs against approved access list, generates exception report; review owner must sign exception register |
| Incomplete change management | CC8.1 | Hotfixes skip ticket workflow | Pre-commit + CI hooks enforce ticket ID in every commit; `soc2-evidence/changes/` audit log is the merge-queue itself |
| Untested backups | A1.2 (Availability) | Backups run, restoration never tested | Quarterly restore-from-backup test cron; result logged to `soc2-evidence/availability/restore-tests/` |
| Stale risk register | CC3.1, CC3.2 | Register written at start of period, never updated | Mandatory risk register review tied to every major change ticket; cron flags > 90 day staleness |
| Policy drift | CC1.1, CC1.2 | Policies versioned but not re-acknowledged after material change | `soc2-evidence/policies/` cron checks acknowledgment recency; > 12 months triggers re-ack campaign |
| Incident response gaps | CC7.4, CC7.5 | Incidents happen, postmortems delayed indefinitely | Incident SLA: postmortem within 5 business days of resolution; `soc2-evidence/incidents/` cron flags overdue |
| Logical access misconfigurations | CC6.1 | MFA not enforced for service accounts, dormant accounts retained | IdP-sync detector flags non-MFA users and accounts inactive > 90 days |

The pattern: each control needs evidence of **operation across the period**, not just **existence at period start**. The shipped cron infrastructure exists precisely to produce that period-wide trail.

---

## 7. Post-Type II surveillance cycle

The first Type II is the hard one. Subsequent cycles are renewals against an already-validated control environment.

### Year 2 shape

- **Observation period extends to 12 months** (industry default after first cycle).
- **Same auditor** (default): keeps continuity; surveillance pricing ~$30-50k assuming year-1 lock at +5%.
- **Switch auditor** (less common): if year-1 auditor was a poor fit, switch; expect +20-30% in year 2 due to onboarding.
- **Same control set, mostly**: changes happen via change-control process (see triggers below).
- **Mid-year bridge letter** issued: certifies controls remained in operation between Type II report dates. Useful for sales (covers the audit gap).

### Ongoing annual cost (steady state, after year 1)

| Line item | Cost |
|---|---|
| Auditor (Type II renewal) | $30-50k |
| Compliance platform (Vanta/Drata/Secureframe) | $15-25k |
| Internal compliance lead (fractional / part of role) | $40-80k loaded |
| Penetration test (annual; SOC 2 expects it though not strictly required) | $15-30k |
| Bug bounty / external attestation supplements | $5-20k |
| **Annual run rate** | **$105-205k** |

### Minor vs major change triggers

**Minor changes (audit-during-cycle, no scope change):**
- Adding a sub-processor (e.g., new SaaS tool)
- Routine personnel changes
- Minor policy updates (typos, clarifications)
- Adding a new monitored asset within existing system boundary

Handling: log in change register, communicate to auditor, no scope renegotiation.

**Major changes (mid-cycle review + possible scope renegotiation):**
- Adding a new TSC (Availability, Confidentiality, Processing Integrity, Privacy)
- Material change to system boundary (acquired a product line, spun out a subsidiary)
- New product with materially different control surface (e.g., adding an on-prem deployment)
- Subservice org change with broad blast radius (changing primary cloud provider)
- Compliance platform swap (Vanta → Drata)
- Security incident with reportable customer impact

Handling: notify auditor within 5 business days; expect scope amendment; possibly issue qualified bridge letter until next full report.

**Trigger-to-action SLA:**
- Detect → log to `soc2-evidence/changes/major-change-register.json`: same day
- Notify auditor: 5 business days
- Scope amendment (if needed): 30 days
- Updated bridge letter: 60 days

### Continuous improvement loop

Each cycle's exceptions become next cycle's preempted failure modes. After year-1 Type II:
1. Review every exception in the report.
2. For each: identify the missing-evidence pattern, encode a new cron / dashboard check in `soc2-evidence/`.
3. Add to the "common failure modes" table in this document for the next operator.
4. Update internal training: AIMS policy ack should mention the new control.

The shipped infrastructure is a living system. Year 2 should have fewer exceptions than year 1; year 3 fewer than year 2. If exceptions are flat across cycles, the infrastructure is decoupled from auditor feedback — fix the feedback loop, not the controls.

---

## Closure

This package assumes ~6 weeks from operator green-light to observation period kickoff:
- Week 1-2: RFP to 4 firms (Schellman, A-LIGN, BARR, Vanta+CPA bundled), apply decision matrix
- Week 3: Select; negotiate engagement letter using template above
- Week 4: Sign; provision auditor access; confirm Day 0 prerequisites
- Week 5: Compliance platform selection + kickoff (if not already in place)
- Week 6: Day 0 kickoff call; observation period begins

End-to-end first Type II: ~9 months from this document (6 months observation + 1 month report drafting + 2 months slack).

Operator: keep this document versioned alongside `compliance/soc2-evidence/`. Any deviation (different weights, different firms, different platform) gets logged here for the next operator.
