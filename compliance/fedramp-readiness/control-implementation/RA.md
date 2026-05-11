# RA — Risk Assessment (NIST SP 800-53r5)

**Family:** RA (Risk Assessment)
**Baseline:** FedRAMP Moderate
**Date:** 2026-05-05

---

## RA-1 — Risk Assessment Policy and Procedures
- **Status:** Partial
- **Evidence:** `agent-foundations/compliance/README.md`, conduct modules (`verification.md`, `failure-modes.md`).
- **Gap:** No standalone Risk Assessment Policy doc.

## RA-2 — Security Categorization
- **Status:** Implemented
- **Evidence:** `ssp-skeleton.md` § 4.2 — FIPS 199 Moderate (Conf=Mod, Int=Mod, Avail=Low).
- **Gap:** Categorization assumes hosted CUI handling; revisit per actual deployment.

## RA-3 — Risk Assessment
- **Status:** Partial
- **Evidence:**
  - `wixie/prompts/security-closure/results/synthesis.md` — security audit + remediation list (F-001 through F-024).
  - `hydra/plugins/vuln-detector/` — supply-chain CVE feed.
  - `hydra/plugins/secret-scanner/` — secret-exposure risk.
  - `hydra/plugins/canary/` — prompt-injection risk monitoring.
- **Gap:** No formal annual RA artifact distinct from the closure synthesis.

## RA-3(1) — Supply Chain Risk Assessment
- **Status:** Implemented
- **Evidence:** `hydra/plugins/package-gate/` + `hydra/plugins/vuln-detector/` + `hydra/plugins/license-gate/` + `hydra/plugins/sbom-emitter/`.
- **Gap:** F-001 SBOM default-off; F-002 no Sigstore/SLSA L3.

## RA-5 — Vulnerability Monitoring and Scanning
- **Status:** Partial
- **Evidence:**
  - **Dependabot** — daily npm/PyPI advisory scans.
  - **GHAS CodeQL** — static analysis on PR + nightly.
  - **OSV-Scanner** cron — planned, F-009.
  - **hydra/plugins/vuln-detector/** — OSV.dev integration.
- **Gap:** F-009 OSV cron not shipped; CodeQL triage backlog (F-022).

## RA-5(2) — Update Vulnerabilities to Be Scanned
- **Status:** Implemented (OSV.dev + Dependabot feeds auto-update)

## RA-5(3) — Breadth / Depth of Coverage
- **Status:** Partial
- **Evidence:** Scans cover all in-boundary repos.
- **Gap:** No container-image scanning (no containers today; will need when hosted).

## RA-5(4) — Discoverable Information
- **Status:** Partial
- **Evidence:** Public repo; vuln disclosure via GitHub Security Advisories.
- **Gap:** No SECURITY.md disclosure-policy file standardized across repos (some have it, not all).

## RA-5(5) — Privileged Access for Scanning
- **Status:** Implemented (CI runs with repo-scoped GitHub token)

## RA-5(6) — Automated Trend Analyses
- **Status:** Partial
- **Evidence:** Dependabot history; `wixie/plugins/inference-engine/` learns vuln-class recurrence.

## RA-5(11) — Public Disclosure Program
- **Status:** Planned (formalize SECURITY.md across all repos)

## RA-7 — Risk Response
- **Status:** Partial
- **Evidence:**
  - Each F-code finding has a runbook in `agent-foundations/runbooks/`.
  - F-001-F-024 closure tracked in `wixie/prompts/security-closure/results/synthesis.md`.
- **Gap:** No formal POA&M artifact (gap list above is POA&M-shaped but not formal).

## RA-9 — Criticality Analysis
- **Status:** Partial
- **Evidence:** `ssp-skeleton.md` § 4 information-type table identifies CUI flow.
- **Gap:** No formal per-component criticality ranking.

## RA-10 — Threat Hunting
- **Status:** Partial
- **Evidence:** `hydra/plugins/canary/` synthetic prompt-injection fixtures; `wixie/plugins/inference-engine/` cross-session pattern detection.
- **Gap:** No human threat-hunt cadence; depends on hosted SOC.

---

## Family-level gaps (top 5)

1. **F-009** OSV-Scanner cron not shipped.
2. **F-022** CodeQL triage backlog.
3. **No formal POA&M artifact** — gap list exists but not in POA&M format.
4. **No annual Risk Assessment doc** distinct from continuous monitoring.
5. **No human threat hunt** — depends on hosted SOC.
