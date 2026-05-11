# Playbook — CC9.2 Vendor and business-partner risk

- **Control ID:** CC9.2
- **Control description:** The entity assesses and manages risks associated with vendors and business partners.
- **Evidence-collection mechanism:** Daily hash of `hydra/plugins/sbom-emitter/state/sbom.cdx.json` (CycloneDX SBOM) plus tail of `hydra/plugins/license-gate/state/findings.jsonl` and `hydra/plugins/vuln-detector/state/audit.jsonl`.
- **Producer (today):** `hydra/plugins/sbom-emitter/`, `hydra/plugins/license-gate/`, `hydra/plugins/package-gate/`, `hydra/plugins/vuln-detector/`.
- **Retention rule:** 7 years.
- **Who reviews:** Repo maintainer weekly.
- **Escalation path:** SBOM stale (>7 days unrotated despite dep changes) → re-emit. **GAP:** F-001 SBOM default-off — must be on before EU CRA 2027 / Type II.
- **Type II evidence shape:** Continuous SBOM-hash + license-findings + vuln-audit log across the window.
- **External dependency:** Upstream advisory feeds (OSV, npm, pip).
