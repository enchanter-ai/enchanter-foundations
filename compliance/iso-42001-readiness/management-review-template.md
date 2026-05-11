# Management Review Template — ISO/IEC 42001 §9.3

Per ISO/IEC 42001 clause §9.3 (Management review). The AIMS owner convenes top management on a quarterly cadence (minimum annual) to review the management system, ensuring continued suitability, adequacy, effectiveness, and alignment with strategic direction.

## Cadence

- **Quarterly** for the first 12 months post AIMS implementation
- **Semi-annual** thereafter unless trigger event (incident, audit finding, regulatory change)
- **Ad-hoc** within 5 working days of any Critical residual-risk event per the risk register

## Mandatory agenda items (ISO 42001 §9.3.2 minimum)

For each quarterly review, the chair MUST cover:

### 1. Status of actions from previous management reviews
- Open action items, due dates, ownership
- Closed items: outcomes, evidence

### 2. Changes in external and internal issues relevant to the AIMS
- Regulatory landscape (EU AI Act updates, NIST AI RMF profile revisions, EU CRA timeline)
- New customer or stakeholder requirements
- Vendor/supplier changes affecting the AI lifecycle (model deprecations, MCP server changes)

### 3. Information on AIMS performance
- KPIs vs targets (incident count, MTTR, false-positive rate, evidence completeness)
- Audit findings (internal + any external)
- Risk register movements (new risks, residual changes, mitigations closed)
- Nonconformities + corrective actions
- Monitoring + measurement results

### 4. Feedback from interested parties
- Customer complaints or escalations
- Regulator interactions
- Developer (internal stakeholder) feedback
- Partner / third-party assessor input

### 5. Adequacy of resources
- Personnel: AIMS owner, AI custodian, AI auditor, security engineer
- Tooling: hydra, wixie, pech, runtime infrastructure
- Budget for compliance evidence collection, external audits, pentest

### 6. Effectiveness of actions taken to address risks and opportunities
- Did mitigations actually reduce residuals?
- Are awareness-only risks (R-021/R-022 alignment faking, sandbagging) progressing toward measurable detection?

### 7. Opportunities for continual improvement
- New mitigations to pilot
- Process simplifications
- Cross-team learnings

## Required outputs (ISO 42001 §9.3.3)

The review MUST produce documented decisions on:

- [ ] Opportunities for improvement
- [ ] Changes needed to the AIMS
- [ ] Resource needs

## Template (fill per session)

---

### Management Review — YYYY-Qn

**Date**: YYYY-MM-DD
**Chair**: ____ (AIMS owner)
**Attendees**: ____ (top management, AI custodian, security engineer, others)
**Quorum**: ____ (per AIMS policy §5.3)

### Agenda item 1 — Prior actions
| ID | Action | Owner | Due | Status | Evidence |
|---|---|---|---|---|---|
| AR-... | ... | ... | ... | open/closed | path to evidence |

### Agenda item 2 — Context changes
- Regulatory: ____
- Customer: ____
- Vendor: ____

### Agenda item 3 — AIMS performance
- KPI summary: ____ (attach dashboard export from `compliance/soc2-evidence/auditor-readiness-dashboard.md`)
- Risk register delta vs last review: ____ new, ____ closed, ____ residual escalations
- Internal audit findings: ____ (link to `internal-audit-checklist.md` output)
- Top 3 corrective actions: ____

### Agenda item 4 — Feedback
- Customer: ____
- Regulator: ____
- Internal: ____

### Agenda item 5 — Resource adequacy
- Personnel: ____
- Tooling: ____
- Budget: ____

### Agenda item 6 — Mitigation effectiveness
- Reductions in residual risk this period: ____
- Mitigations that did NOT achieve target: ____ (root cause + new action)

### Agenda item 7 — Improvement opportunities
- ____
- ____

### Decisions (binding outputs)

| ID | Decision | Owner | Due | Resource impact |
|---|---|---|---|---|
| MR-YYYY-Qn-001 | ... | ... | ... | ... |

### Sign-off
- AIMS owner: ____
- Top management: ____
- Minutes archived to: `compliance/iso-42001-readiness/management-reviews/YYYY-Qn.md`

---

## Cert-body audit consideration

ISO 42001 cert bodies (BSI, DNV, TÜV) explicitly check that:
- Management review actually happens (calendar evidence)
- Minutes are documented and signed
- Decisions flow into actionable items with owners + due dates
- Prior actions are reviewed at next session (the "you said you'd do X — did you?" loop)

**Missing management reviews is a Stage-2 audit failure trigger.** First review must happen before the cert body's Stage 2 audit.

## Initial reviews to schedule (operator action)

- **2026-Q3** (≤ 2026-09-30): first review post AIMS implementation
- **2026-Q4** (≤ 2026-12-31): second review
- **2027-Q1**: third review (typically targeted before cert-body Stage 1)
- **Cadence then settles to semi-annual** per §1 unless trigger event
