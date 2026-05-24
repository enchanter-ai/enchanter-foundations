# ISO/IEC 42001 Certification Engagement Package

**Audience:** Compliance lead + engineering exec preparing the AIMS (AI Management System) for third-party certification.
**Scope:** Selecting an accredited certification body, navigating Stage 1 (documentation review) and Stage 2 (implementation audit), and maintaining the certificate across the three-year cycle.
**Prerequisite:** Internal readiness pack at `packages/safety/compliance/iso-42001-readiness/` is drafted and minutes from Management Review #1 exist. If that pack is not yet in place, complete Section 2 (Pre-engagement readiness) before requesting cert-body quotes — quotes anchor to scope, and scope without a Statement of Applicability is a guess.
**Status of figures:** All pricing in this document is **estimated** from public references, vendor sales conversations, and 2025-era engagement post-mortems. Quotes must be obtained directly; treat the ranges as planning anchors, not commitments.

---

## 1. Certification body comparison

ISO/IEC 42001 was published 2023-12. Accreditation for cert bodies under UKAS (UK) and ANAB (US, via ANSI National Accreditation Board) ramped through 2024-2025. Most major IMS (Integrated Management System) bodies offer 42001 today, but AI-specific track record is the differentiator — a body that has issued only 5-10 42001 certs will reuse 27001 auditors with a thin AI briefing, which surfaces as weaker Annex A coverage during Stage 2.

### 1.1 Established IMS bodies

| Body | 42001 accreditation | AI-specific track record | Stage 1+2 (Year 1, est.) | Surveillance Y2 / Y3 (est.) | Geo coverage | Lead time |
|------|---------------------|--------------------------|--------------------------|------------------------------|--------------|-----------|
| **BSI Group** (https://www.bsigroup.com/en-GB/products-and-services/standards/iso-iec-42001-ai-management-system/) | UKAS-accredited 42001 (first body globally, Feb 2024) | Strongest — co-authored the standard via committee; 100+ 42001 certs issued globally by Q1 2026 | $35-55k | $12-20k / $12-20k | Global (60+ countries) | 14-20 weeks from kick-off |
| **DNV** (https://www.dnv.com/services/iso-iec-42001-artificial-intelligence-management-system-certification-243947) | UKAS + ANAB | Strong — heavy in EU regulated industries (maritime, energy, healthcare AI) | $30-50k | $10-18k / $10-18k | Global, EU-strongest | 12-18 weeks |
| **TÜV SÜD** (https://www.tuvsud.com/en/services/auditing-and-system-certification/iso-iec-42001) | DAkkS (Germany) + UKAS | Strong — known for industrial AI, automotive, medical devices; tight on Annex A.6 (impact assessment) | $35-60k | $14-22k / $14-22k | Global, EU/DACH-strongest | 14-22 weeks |
| **TÜV Rheinland** (https://www.tuv.com/landingpage/en/iso-iec-42001/) | DAkkS + ANAB | Moderate-strong — overlaps TÜV SÜD turf; differentiator is faster turnaround in US | $30-50k | $11-18k / $11-18k | Global, EU/US balanced | 12-16 weeks |
| **SGS** (https://www.sgs.com/en/services/iso-iec-42001-aims-certification) | UKAS + ANAB | Moderate — broad IMS portfolio, AI specialism is newer (2024-onward); pricing competitive | $25-45k | $9-16k / $9-16k | Global, broadest geographic footprint of any body listed | 10-16 weeks |
| **Bureau Veritas** (https://www.bureauveritas.com/services-plus-solutions/iso-42001-artificial-intelligence-management-system-certification) | UKAS + ANAB | Moderate — strong in finance/insurance AI; weaker public track record on pure-play AI SaaS | $28-48k | $10-17k / $10-17k | Global | 12-18 weeks |

### 1.2 AI-focused / newer entrants

| Body | 42001 accreditation | AI-specific track record | Stage 1+2 (Year 1, est.) | Surveillance Y2 / Y3 (est.) | Geo coverage | Lead time |
|------|---------------------|--------------------------|--------------------------|------------------------------|--------------|-----------|
| **A-LIGN** (https://www.a-lign.com/services/iso-42001) | ANAB | Moderate — SOC 2 / ISO 27001 specialist pivoting into 42001; strong for US tech orgs already in their ecosystem | $25-40k | $8-14k / $8-14k | US-primary, EU via partner | 8-14 weeks |
| **Schellman** (https://www.schellman.com/iso-42001) | ANAB | Moderate-strong — early ANAB-accredited 42001 body, US tech-first; bundles well with SOC 2 + 27001 | $28-45k | $9-15k / $9-15k | US-primary | 8-12 weeks |
| **Mastermind / Coalfire / Insight Assurance** | ANAB (varies) | Light-moderate — emerging; verify accreditation status at quote time | $20-35k | $7-12k / $7-12k | US-primary | 8-12 weeks |
| **HKQAA, JQA, JIPDEC** (regional) | Regional accreditation | Light on AI; strong domestic recognition | Varies, often lower | Varies | APAC | Varies |

### 1.3 Reading the table

- **Year-1 totals** assume a single-site AIMS scope covering one to three AI products with ≤ 200 personnel in scope. Multi-site or > 500 personnel adds 25-50%.
- **Day rates** drive the totals: BSI / TÜV SÜD anchor around $2,500-3,200/day; SGS / Schellman / A-LIGN around $1,800-2,500/day; emerging US-tech-focused bodies $1,500-2,200/day. Stage 1 is typically 2-4 audit-days; Stage 2 is 5-10.
- **Surveillance audits** at year 2 and year 3 are roughly 40-50% of the Stage 2 effort. Recertification at year 3 is roughly 80% of the original Year-1 cost.
- **Lead time** is the gap between signed engagement letter and Stage 1 onsite. UKAS-accredited bodies were back-logged through most of 2025; expect 12+ weeks for BSI/DNV/TÜV SÜD, 8-12 for Schellman/A-LIGN.

---

## 2. Pre-engagement readiness assessment

Run this checklist against the existing pack at `packages/safety/compliance/iso-42001-readiness/` before requesting quotes. Every "no" is a Stage 1 or Stage 2 finding waiting to happen.

### 2.1 Clause 4 — Context of the organization

- [ ] `iso-42001-readiness/clause-4/context-of-organization.md` documents internal/external issues, interested parties (regulators, customers, employees, society), and AIMS scope statement.
- [ ] Scope statement names the AI systems in scope (model families, deployment surfaces) and exclusions with justification.
- [ ] Interested-party register reviewed within last 12 months.

### 2.2 Clause 5 — Leadership

- [ ] AIMS policy signed by top management within last 12 months (`iso-42001-readiness/clause-5/aims-policy.md`).
- [ ] Roles, responsibilities, and authorities documented and assigned by name, not just by title (`iso-42001-readiness/clause-5/raci.md`).
- [ ] Top management's accountability for AIMS effectiveness is demonstrable via Management Review minutes (see 2.6).

### 2.3 Clause 6 — Planning

- [ ] AI risk register (`iso-42001-readiness/clause-6/ai-risk-register.xlsx` or `.md`) — current within 90 days, covering at minimum: bias/fairness, robustness, privacy, security, transparency, accountability, environmental impact.
- [ ] AI impact assessments for each in-scope AI system (`iso-42001-readiness/clause-6/aiia/`) — per ISO/IEC 42005 guidance.
- [ ] AIMS objectives are SMART, owner-assigned, with measurement cadence (`iso-42001-readiness/clause-6/objectives.md`).
- [ ] Treatment plan exists for each unacceptable residual risk.

### 2.4 Clause 7 — Support

- [ ] Resources, competence, awareness, communication, documented information clauses each have a one-pager (`iso-42001-readiness/clause-7/`).
- [ ] Competence matrix evidences training of personnel on AI risks, AIMS responsibilities, and incident response.

### 2.5 Clause 8 — Operation

- [ ] Operational planning and control: ML lifecycle, data management, model deployment runbooks linked (`iso-42001-readiness/clause-8/operational-controls.md`).
- [ ] AI system impact assessments operationalized — each new model release triggers the assessment workflow.
- [ ] Data quality and provenance controls (`iso-42001-readiness/clause-8/data-management.md`).
- [ ] Third-party / supplier AI controls (`iso-42001-readiness/clause-8/supplier-controls.md`).

### 2.6 Clause 9 — Performance evaluation

- [ ] Monitoring/measurement plan with KPIs for each AIMS objective (`iso-42001-readiness/clause-9/monitoring.md`).
- [ ] **Internal audit #1 completed** with audit report, nonconformity log, and closure evidence (`iso-42001-readiness/clause-9/internal-audit-1/`). **This is a Stage 2 gating item.**
- [ ] **Management Review #1 minuted** covering all required inputs (audit results, KPI trends, risk changes, opportunities for improvement) and all required outputs (decisions, actions, resources). (`iso-42001-readiness/clause-9/management-review-1.md`). **Also a Stage 2 gating item.**

### 2.7 Clause 10 — Improvement

- [ ] Nonconformity and corrective action procedure with worked examples from the last cycle (`iso-42001-readiness/clause-10/ncar-procedure.md`).
- [ ] Continual improvement evidence — at least 3 closed improvements traceable to MR #1 or internal audit findings.

### 2.8 Annex A — Statement of Applicability (SoA)

- [ ] SoA (`iso-42001-readiness/soa.xlsx` or `.md`) covers all Annex A controls (A.2 through A.10) with: applicable Y/N, justification, implementation reference, evidence pointer.
- [ ] No Annex A control marked "N/A" without written justification.
- [ ] Each "applicable" control has at least one piece of implementation evidence (procedure, log, configuration, training record).

### 2.9 Readiness gate

If any of the bolded items above are "no" — internal audit #1, management review #1, SoA — **do not engage a cert body yet.** Stage 1 will fail and you'll burn the engagement fee on a dry run.

---

## 3. Stage 1 preparation timeline — 8 weeks

Stage 1 is a documentation and readiness review. The cert body confirms the AIMS exists on paper and you're ready for the implementation audit. Findings are usually "areas of concern" rather than nonconformities — but unresolved areas of concern become Stage 2 NCs.

### Weeks 1-2: Internal audit dry-run

- Re-run the internal audit (clause 9.2) against the full clause-4-to-10 + Annex A checklist as if you were an external auditor.
- Audit team must be independent of the area audited (i.e., the ML team doesn't audit ML processes).
- Output: refreshed nonconformity log with severities (minor / major / observation).

### Weeks 3-4: Close minor nonconformities

- Close every minor NC from the dry run. Document root cause, correction, corrective action.
- Defer major NCs only if they truly cannot be closed in 8 weeks — but flag them in your cert-body application so the auditor isn't surprised.
- Refresh Management Review minutes if any closure changes the risk profile.

### Week 5: Cert body application + contract

- Submit application to selected cert body (see Section 6 for decision matrix). Application requires: AIMS scope statement, number of personnel, sites, AI systems in scope, prior certifications (ISO 27001, SOC 2).
- Cert body returns a proposal with day count and price. Sign within the week; lead time runs from signature.

### Weeks 6-7: Stage 1 documentation package

- Compile the Stage 1 evidence package — auditors request this 2-3 weeks pre-onsite:
  - AIMS policy, scope, objectives
  - SoA + Annex A evidence
  - Internal audit #1 report + NC closure evidence
  - Management Review #1 minutes
  - Risk register + treatment plan
  - AI impact assessments for in-scope systems
  - Org chart + RACI
- Upload to the cert body's audit portal (most use proprietary portals; some accept Drive/SharePoint shares).

### Week 8: Stage 1 onsite (or remote)

- 2-4 audit-days. Auditor reviews the documentation package, interviews top management + AIMS owner, walks through 2-3 sample controls.
- Output: Stage 1 report listing readiness for Stage 2 + any areas of concern.
- **Decision point:** Stage 2 can proceed only after Stage 1 closure. If major findings surface, expect a 4-8 week gap before Stage 2.

---

## 4. Stage 2 preparation timeline — 8-12 weeks post-Stage 1

Stage 2 is the implementation audit. The auditor traces controls from policy through implementation to evidence, interviews personnel at all levels, and tests sampled processes end-to-end.

### Weeks 1-3 post-Stage 1: Gap closure

- Address every Stage 1 area of concern with documented action.
- For each finding, produce: root cause, correction, corrective action, evidence of effectiveness, closure date.
- If a finding touches a recurring process, run the process at least once post-fix to demonstrate the corrective action works.

### Weeks 4-6: Evidence dossier compilation

- Build a per-control evidence dossier indexed against the SoA. Each Annex A control should have ≥ 2 pieces of evidence from the last 90 days (logs, screenshots, signed documents, training records).
- Specifically over-prepare on the controls in Section 5 (common findings) — those are the auditor's hot list.
- Evidence freshness matters: a 2024 training record won't carry a 2026 audit.

### Weeks 7-9: Personnel interview prep

- Auditors sample 5-15 personnel across roles: top management, AIMS owner, ML engineers, data engineers, security, legal, customer-facing.
- Each interviewee should be able to:
  - State their role in the AIMS in one sentence
  - Name the AIMS policy and where to find it
  - Describe one AI risk relevant to their work and how it's controlled
  - Describe the incident response path for an AI failure
- Run mock interviews in week 7-8. The most common Stage 2 finding from personnel interviews is **inconsistency between policy and practice** — a documented control that nobody on the team can describe.

### Weeks 10-11: Walkthrough rehearsal

- Pick 3-5 sample AI systems and rehearse end-to-end walkthroughs: design → risk assessment → data sourcing → training → evaluation → deployment → monitoring → incident handling.
- Time-box each walkthrough to 60-90 minutes. Stage 2 walkthroughs run that long; rehearse to that bound.

### Week 12: Stage 2 audit window

- 5-10 audit-days depending on scope. Onsite or remote (most bodies accept remote post-2024).
- Closing meeting on the final day: auditor presents draft findings.
- 2-4 weeks post-audit: final report + cert decision. Major NCs require 90-day closure plan; minor NCs require 90-day evidence of corrective action.

---

## 5. Common Stage 1 + Stage 2 findings

Surveyed from publicly available audit summaries (BSI, DNV, Schellman case studies 2024-2025), ISO/IEC JTC 1/SC 42 working group post-mortems, and certified-org disclosures.

### 5.1 Top 10 findings + preemptive mitigations

| # | Finding | Root cause | Preemptive mitigation |
|---|---------|-----------|------------------------|
| 1 | **SoA control marked applicable but no evidence** | Control adopted from template, not operationalized | Audit each "applicable" row in `iso-42001-readiness/soa.md` for ≥ 2 evidence artifacts dated within 90 days |
| 2 | **AI impact assessments stale or missing for recent model releases** | Process exists but doesn't fire on every release | Wire the AIIA into the release checklist (`iso-42001-readiness/clause-6/aiia/release-trigger.md`); evidence the last 3 releases each have one |
| 3 | **Risk register not reviewed within 90 days** | Quarterly cadence slipped | Calendar invite + MR agenda item; refresh `iso-42001-readiness/clause-6/ai-risk-register.md` no less than 90 days pre-Stage 1 |
| 4 | **Top management cannot articulate AIMS objectives** | Policy signed but not internalized | One-page exec brief; rehearse the interview in week 7-8 of Section 4 |
| 5 | **Personnel inconsistent on incident response path** | Procedure exists but training is patchy | Tabletop exercise documented in `iso-42001-readiness/clause-8/incident-response-tabletop.md`; refresh competence matrix |
| 6 | **No evidence of supplier AI controls** | Vendor onboarding doesn't include AI-specific clauses | Updated DPA / supplier addendum at `iso-42001-readiness/clause-8/supplier-controls.md`; evidence: 2-3 executed addenda |
| 7 | **Data provenance gaps on training datasets** | Older datasets ingested without lineage metadata | Lineage register at `iso-42001-readiness/clause-8/data-management.md`; remediate top 5 datasets minimum |
| 8 | **Internal audit didn't cover all clauses + Annex A** | Audit scope drift | Audit plan template explicitly enumerates clauses 4-10 + every applicable Annex A control (`iso-42001-readiness/clause-9/internal-audit-plan.md`) |
| 9 | **Management Review missed required inputs/outputs** | MR minutes informal | Template at `iso-42001-readiness/clause-9/management-review-template.md` with the 9.3.2 input list and 9.3.3 output list as headers |
| 10 | **Continual improvement not traceable to inputs** | Improvements happen but aren't logged against findings | Improvement log links each closed item to its source (audit / MR / incident / complaint) at `iso-42001-readiness/clause-10/improvement-log.md` |

### 5.2 AI-specific findings (rarer in 27001, common in 42001)

- **Bias / fairness controls described abstractly without metrics.** Auditor wants to see the metric (demographic parity, equalized odds, etc.), the threshold, the monitoring cadence, the action on breach.
- **No transparency artifact for in-scope systems.** Model cards, system cards, or equivalent — referenced in `iso-42001-readiness/clause-8/transparency-artifacts/`.
- **Human oversight described, not designed.** Auditor wants to see the human-in-the-loop control point in the actual product flow, with logs of human decisions.
- **Environmental impact omitted.** Annex A.6.2.2 is explicit; have a one-page energy / compute footprint estimate per in-scope system.

---

## 6. Decision matrix

Weighted criteria for selecting among the bodies in Section 1.

| Criterion | Weight | Score 1-5 per body | Weighted |
|-----------|--------|--------------------|----------|
| AI-specific expertise (track record, AI-trained auditors, published guidance) | 35% | per body | × 0.35 |
| Pricing (Year-1 total + 3-year TCO) | 25% | per body | × 0.25 |
| Geographic + lead time fit (audit-team location, time-zone alignment, weeks-to-Stage-1) | 20% | per body | × 0.20 |
| Surveillance terms (Y2/Y3 pricing, scope flexibility, re-audit triggers) | 10% | per body | × 0.10 |
| Reputation / customer recognition (does the cert carry weight with our customers?) | 10% | per body | × 0.10 |

### 6.1 Default ranking for a US-primary, EU-secondary AI SaaS

Based on the weights above and the public information in Section 1:

1. **BSI** — top on AI expertise + reputation; mid on pricing; long lead time is the main drag.
2. **Schellman** — top on US lead time + bundle with SOC 2 / 27001; mid on AI expertise.
3. **DNV** — top in regulated-industry recognition; competitive pricing; strong EU coverage.
4. **TÜV SÜD** — top for DACH / industrial customer base; otherwise comparable to DNV.
5. **A-LIGN** — strong if already in their SOC 2 / 27001 program; lower reputation weight than BSI.
6. **Bureau Veritas / SGS / TÜV Rheinland** — viable mid-tier choices; pick on geographic fit.

### 6.2 When to deviate

- **Customer mandate.** If a flagship customer requires a specific body, that body wins regardless of matrix score.
- **Regulated sector.** Healthcare → DNV/TÜV SÜD. Automotive → TÜV SÜD/TÜV Rheinland. Financial services → BSI/Bureau Veritas.
- **Bundle economics.** If SOC 2 and 27001 are also in play, bundled-audit savings with Schellman / A-LIGN can exceed BSI's reputation premium.

---

## 7. Surveillance cycle

ISO 42001 certificates are valid 3 years, with annual surveillance audits.

### 7.1 Year 2 surveillance

- **Scope:** ~40-50% of Stage 2 effort. 2-5 audit-days.
- **Auditor priorities:** evidence that the AIMS is operating (not just documented), closure of any Year-1 NCs, Management Review and internal audit conducted since cert, risk register refreshed, sampled controls.
- **Common Year-2 trip wires:** the MR / internal audit cadence slips because the urgency drained after cert. Calendar these immediately post-cert.

### 7.2 Year 3 surveillance + recertification

- **Surveillance:** same as Year 2.
- **Recertification:** runs alongside Year-3 surveillance or in the following months. ~80% of Year-1 cost. Full clause + Annex A coverage, but with the auditor's accumulated familiarity reducing onboarding overhead.
- **Output:** new 3-year certificate.

### 7.3 Year-on-year cost envelope (estimated)

For a single-site, three-AI-product, ~200-person scope:

| Year | Activity | Estimated cost |
|------|----------|----------------|
| Y1 | Stage 1 + Stage 2 | $25-60k |
| Y2 | Surveillance | $8-22k |
| Y3 | Surveillance + recert | $25-50k |
| **3-year TCO** | | **$58-132k** |

---

## 8. Certificate maintenance — what triggers a re-audit

Outside the scheduled cycle, the following changes require notifying the cert body and may trigger a special audit (typically 1-3 days, charged at day rate):

### 8.1 Mandatory notification

- **Major AIMS scope change** — new AI system added to scope, new site, scope expansion to a new business unit, or scope reduction (the body confirms the reduction doesn't invalidate the cert).
- **Top management change** — new CEO / AIMS sponsor; the body confirms continuity of leadership commitment.
- **Significant regulatory shift affecting in-scope AI** — e.g., EU AI Act enforcement milestones, NIST AI RMF amendments, sector-specific AI rules that materially change controls.
- **Major nonconformity not closed within 90 days** — escalates to suspension review.
- **Serious AI incident** — material customer / regulator / public-facing incident; the body may run an unannounced or special surveillance audit per IAF MD 4 guidance.

### 8.2 Optional notification / recommended

- **Material residual-risk escalation** — a risk previously rated acceptable now exceeds the tolerance threshold, with no immediate treatment plan.
- **Material technology shift** — moving from in-house models to a third-party foundation model (or vice versa) — changes supplier-control surface materially.
- **Acquisition / divestiture** affecting the AI portfolio.

### 8.3 Triggers for early recertification

Rare, but worth knowing:

- Cumulative scope changes have made the original scope statement materially inaccurate.
- The body's accreditation lapses or transfers (very rare; you may need to migrate the cert).
- Standard revision (a hypothetical ISO 42001:2028) — transition window is typically 2-3 years.

### 8.4 Maintenance discipline

The cheapest path to a clean Year-2 and Year-3 audit is **operating the AIMS as if the cert body could walk in any week**. Concretely:

- Quarterly risk register refresh (calendar invite, never skipped).
- Quarterly Management Review (lighter cadence than the pre-cert one, but still minuted with the 9.3.2/9.3.3 structure).
- Annual internal audit + annual full Management Review.
- Continuous improvement log updated within 5 business days of any incident, finding, or customer complaint touching AI.

Drift here is the single biggest predictor of a hostile Year-2 surveillance.

---

## 9. Engagement checklist (one-page summary)

Pre-engagement:
- [ ] Section 2 readiness checklist all green
- [ ] Internal audit #1 closed
- [ ] Management Review #1 minuted
- [ ] SoA evidenced ≥ 2 artifacts per applicable control

Body selection:
- [ ] Decision matrix (Section 6) scored across at least 3 bodies
- [ ] 2-3 quotes obtained and compared on like-for-like scope
- [ ] Customer/regulatory constraints applied per Section 6.2

Stage 1 (8 weeks):
- [ ] Internal audit dry-run → NC closure → application → docs package → onsite

Stage 2 (8-12 weeks post-Stage 1):
- [ ] Gap closure → dossier → interview prep → walkthrough rehearsal → audit window

Post-cert:
- [ ] Y2 + Y3 surveillance calendared on day-1 post-cert
- [ ] Change-notification triggers (Section 8) wired into change-management policy
- [ ] Recertification budget allocated in Y3

---

**Document version:** v1 (2026-05-05)
**Next review:** post-Stage 1 walkthrough, or 2026-Q4, whichever first.
**Owner:** Compliance lead.
**References:** `packages/safety/compliance/iso-42001-readiness/` (full readiness pack), `roadmap-2026/MACRO_ROADMAP.md` (program-level context).
