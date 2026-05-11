# SOC 2 External Engagement — Scoping Document

**Purpose:** Define what the enchanter-ai project provides to an independent CPA firm at engagement start, what the firm provides in return, and where the boundary sits between in-house infrastructure and external audit work.

**Status:** Pre-engagement scoping. No CPA firm engaged.

---

## 1. What we ship (already in place)

When the CPA firm arrives, they receive:

| Item | Source-of-truth |
|---|---|
| Control mapping (CC1-CC9 + A1.x) | `agent-foundations/compliance/soc2.md` |
| Evidence-collection plan | `agent-foundations/compliance/soc2-evidence/evidence-collection-plan.md` |
| Daily evidence archive | `agent-foundations/compliance/soc2-evidence/collected/YYYY-MM-DD/` (signed by cosign daily) |
| Per-criterion playbooks | `agent-foundations/compliance/soc2-evidence/playbooks/*.md` |
| Auditor-readiness dashboard | `agent-foundations/compliance/soc2-evidence/auditor-readiness-dashboard.md` |
| HMAC-chained audit log | `hydra/plugins/audit-trail/state/log.jsonl` |
| SBOM (CycloneDX) | `hydra/plugins/sbom-emitter/state/sbom.cdx.json` |
| Pattern catalog (SPRT) | `wixie/plugins/inference-engine/state/catalog.json` |
| Risk register | `wixie/prompts/security-closure/results/synthesis.md` |
| Conduct modules | `agent-foundations/shared/conduct/*.md` |
| Per-prompt artifacts | `wixie/prompts/<name>/{metadata.json, tests.json, learnings.md}` |

All artifacts are git-versioned and cryptographically signed at the daily-bundle level (cosign keyless OIDC via GitHub Actions).

## 2. Access requirements (what the auditor needs from us)

The auditor will need:

- **Read access to the GitHub org** containing the 11 repos (or a snapshot tarball at engagement start + delta tarballs monthly).
- **Read access to the `soc2-evidence` branch** containing daily evidence PRs.
- **Read access to the cosign attestation transparency log** (Rekor — publicly readable, but we provide the entry pointers).
- **Maintainer interview slots** — see Section 5 below.
- **Walkthrough sessions** for the inference-engine, hydra defensive plugins, and the convergence engine.

The auditor does **not** need:

- Write access to any repo (verification, not modification).
- Production-credential access (no production system today; substrate is developer-local).
- Customer-data access (no customer data processed by the substrate itself).

## 3. What the auditor brings (external — NOT in this infrastructure)

| Item | Provided by | Notes |
|---|---|---|
| Independent CPA firm engagement letter | The firm | Contract scope, fees, period. |
| SOC 2 Type II opinion letter | The firm | The actual audit deliverable. |
| Management assertion letter | We draft, firm reviews | Asserts that controls operate effectively. |
| System description (Section 3 of SOC 2 report) | We draft, firm reviews | Narrative of services, infrastructure, controls. |
| SAR (System Assessment Report for FedRAMP overlap) | The firm, if FedRAMP scope is added | Currently out of scope per `fedramp-boundary.md`. |
| Management letter on findings | The firm | Issued at audit close. |
| Type II audit period | The firm + us | 6-12 months of operating effectiveness evidence. |

## 4. Engagement timeline (typical Type II)

| Phase | Duration | Activity |
|---|---|---|
| Scoping | 2-4 weeks | Engagement letter, scope, trust criteria, observation period start |
| Type I (optional, recommended first) | 4-8 weeks of field work | Point-in-time design + implementation opinion |
| Type II observation | **6 months minimum** | Evidence accrues here — our infrastructure does this automatically |
| Type II field work | 4-8 weeks | Auditor reviews evidence, samples, interviews, walkthroughs |
| Report delivery | 2-4 weeks | Draft → management response → final report |

**Realistic earliest Type II report delivery from today (2026-05-05):** ~9 months — 6 months observation + 3 months scoping/field/delivery — **assuming MUST-SHIP queue closes within 30 days** (F-001 SBOM default-on, F-002 weaver-gate, F-004 canary CI gate, F-005 egress allowlist density, F-010 capability-fence CI tests, F-013 rate-limiting).

## 5. Interview schedule template

The auditor will request interviews with the responsible parties for each criterion family. Template:

| Interviewee | Topics | Duration |
|---|---|---|
| Repo maintainer | Org structure (CC1), change management (CC8), risk register (CC3, CC9) | 90 min |
| Security-closure owner | Risk assessment (CC3), monitoring (CC4), incident response (CC7) | 90 min |
| Hydra plugin owner | Technology controls (CC5.2), logical access (CC6), threat protection (CC6.6/6.7/6.8) | 90 min |
| Wixie plugin owner | Communications (CC2), DEPLOY bar (CC3.1), change management (CC8), inference substrate (CC4.1) | 60 min |
| Availability owner (pech/emu) | Capacity (A1.1), backup/recovery (A1.2/A1.3) | 60 min |

Walkthroughs (auditor present, we demonstrate):

- HMAC chain head verification on `hydra/plugins/audit-trail/state/log.jsonl`.
- `inference-engine.py reconcile` run + briefing render.
- `collect-evidence.py` + `evidence-completeness-check.py` daily cron output review.
- One full convergence cycle on a sample prompt (DEPLOY/HOLD/FAIL verdict path).

## 6. Cost expectations (rough order)

| Phase | Range |
|---|---|
| Type I audit | $15k - $40k |
| Type II audit (6mo) | $40k - $100k |
| Annual Type II renewal | $30k - $80k |

These are external CPA firm costs and are **not** budget items for this infrastructure project. Numbers are market estimates as of 2026 — confirm at engagement scoping.

## 7. Honest gaps the auditor will surface (from soc2.md § 14)

The auditor will identify, at minimum, the following open gaps already self-disclosed:

1. CC1.2 — no board / formal oversight structure (single-maintainer).
2. CC5.2 / CC6.1 — F-010 capability-fence CI tests absent.
3. CC6.6 / CC6.7 — F-005 egress allowlist sparse; F-004 canary CI-blocking gate not wired.
4. CC6.8 — F-023 typosquat seed list not registry-derived.
5. CC7.1 — F-009 OSV-Scanner cron not wired.
6. CC7.2 — F-021/F-024 OTLP exporter not shipped.
7. CC7.4 — F-011 pager.ts not shipped.
8. CC9.2 — F-001 SBOM default-off.
9. A1.1 — F-013 multi-tenant rate-limiting absent.
10. A1.3 — no formal recovery-drill schedule.

A Type I engagement can ship today with these gaps documented as remediation items. A Type II engagement requires the MUST-SHIP queue closed before the observation period begins.

## 8. What stays explicitly external

To reiterate from soc2.md § 16 — this infrastructure does NOT produce:

- A SOC 2 Type I or Type II report.
- An independent attestation that controls operated effectively.
- A management assertion letter (drafted at engagement, not here).
- An auditor's opinion or management letter.

This infrastructure is **input** to those — the audit-ready surface, not the audit.
