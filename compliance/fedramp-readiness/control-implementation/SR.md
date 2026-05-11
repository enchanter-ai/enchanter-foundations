# SR — Supply Chain Risk Management (NIST SP 800-53r5)

**Family:** SR (Supply Chain Risk Management)
**Baseline:** FedRAMP Moderate
**Date:** 2026-05-05

---

## SR-1 — Policy and Procedures
- **Status:** Partial
- **Evidence:** `hydra/plugins/package-gate/`, `hydra/plugins/sbom-emitter/`, `hydra/plugins/license-gate/`, `hydra/plugins/vuln-detector/` plugin READMEs.

## SR-2 — Supply Chain Risk Management Plan
- **Status:** Partial
- **Evidence:** Combined plugin defenses constitute the de-facto plan; documented across this folder.
- **Gap:** No standalone SCRM Plan artifact.

## SR-2(1) — Establish SCRM Team
- **Status:** N/A (small org; single maintainer = SCRM owner)

## SR-3 — Supply Chain Controls and Processes
- **Status:** Partial
- **Evidence:**
  - `hydra/plugins/package-gate/` typosquat detection + allowlist on every new dep.
  - `hydra/plugins/sbom-emitter/` CycloneDX SBOM on release (gap: F-001 default-off).
  - `hydra/plugins/license-gate/` rejects copyleft incompatibilities.
  - `hydra/plugins/vuln-detector/` OSV.dev integration.
  - Dependabot daily.
  - GHAS CodeQL on PR + nightly.
- **Gap:** F-001 SBOM default-off; F-002 no Sigstore/SLSA L3 release pipeline.

## SR-3(1) — Diverse Supply Base
- **Status:** N/A (small dep set; diverse upstreams)

## SR-3(2) — Limit Harm
- **Status:** Implemented
- **Evidence:** egress-shield + capability-fence + action-guard collectively limit blast radius of any compromised dep.

## SR-3(3) — Sub-Tier Flow Down
- **Status:** Partial
- **Evidence:** SBOM transitively enumerates sub-tier deps.

## SR-4 — Provenance
- **Status:** Partial
- **Evidence:**
  - npm + PyPI lockfiles pin exact versions + integrity hashes.
  - SBOM emitter records source URL + hash per component.
- **Gap:** F-002 — no Sigstore signing on our own release artifacts; downstream consumers cannot verify our provenance.

## SR-4(1) — Identity
- **Status:** Partial
- **Evidence:** Lockfile + SBOM identify each component by name + version + hash.

## SR-4(2) — Track and Trace
- **Status:** Partial
- **Evidence:** SBOM at every release; git history; audit-trail logs dep installs.

## SR-4(3) — Validate as Genuine and Not Altered
- **Status:** Partial
- **Evidence:** Lockfile integrity hashes (npm `sha512-...`, PyPI hashes).
- **Gap:** Signed-package verification (e.g., sigstore) for direct deps not enforced.

## SR-4(4) — Supply Chain Integrity — Pedigree
- **Status:** Planned (SLSA L3)

## SR-5 — Acquisition Strategies, Tools, and Methods
- **Status:** Implemented (allowlist-based)
- **Evidence:** `hydra/plugins/package-gate/config/allowlist.yaml` declares vetted package names + version ranges.

## SR-6 — Supplier Assessments and Reviews
- **Status:** Partial
- **Evidence:** OSV.dev vuln history; GitHub Security Advisories; license check.
- **Gap:** No formal supplier-review process; relies on automated feeds.

## SR-6(1) — Testing and Analysis
- **Status:** Partial
- **Evidence:** CodeQL static analysis on PRs (covers our code + direct dep call patterns).

## SR-7 — Supply Chain Operations Security
- **Status:** N/A (open source; no operational secrecy)

## SR-8 — Notification Agreements
- **Status:** N/A (consume public OSV.dev feed)

## SR-9 — Tamper Resistance and Detection
- **Status:** Partial
- **Evidence:**
  - Lockfile integrity hashes detect modified packages.
  - audit-trail HMAC chain detects in-system tampering.
  - SBOM hash provides post-install verification.
- **Gap:** F-002 — no SLSA L3 build-attestation; we cannot prove our own build artifacts are tamper-resistant.

## SR-9(1) — Multiple Stages of System Development Life Cycle
- **Status:** Partial
- **Evidence:** package-gate (acquisition), Dependabot (operations), SBOM (release).

## SR-10 — Inspection of Systems or Components
- **Status:** Partial
- **Evidence:** CodeQL nightly + Dependabot + manual triage.

## SR-11 — Component Authenticity
- **Status:** Partial
- **Evidence:** Lockfile hashes + npm/PyPI registry signatures (when present).
- **Gap:** F-002 SLSA L3 not yet on our own releases.

## SR-11(1) — Anti-Counterfeit Training
- **Status:** Partial
- **Evidence:** Conduct module `tool-use.md` warns on typosquats; package-gate enforces.

## SR-11(2) — Configuration Control for Component Service / Repair
- **Status:** N/A (no hardware)

## SR-11(3) — Anti-Counterfeit Scanning
- **Status:** Implemented (package-gate typosquat detection)

## SR-12 — Component Disposal
- **Status:** Implemented (npm uninstall / pip uninstall removes via lockfile + node_modules cleanup)

---

## Family-level gaps (top 5)

1. **F-001** SBOM default-off — SR-4, SR-9 partial.
2. **F-002** No Sigstore/SLSA L3 release — SR-4(4), SR-9(2), SR-11 blocked.
3. **No formal SCRM Plan artifact.**
4. **No signed-package verification on direct deps** — SR-4(3) partial.
5. **No formal supplier-review process** — SR-6 relies on automated feeds only.
