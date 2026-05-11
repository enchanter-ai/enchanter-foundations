# CM — Configuration Management (NIST SP 800-53r5)

**Family:** CM (Configuration Management)
**Baseline:** FedRAMP Moderate
**Date:** 2026-05-05

---

## CM-1 — Configuration Management Policy and Procedures
- **Status:** Partial
- **Evidence:** `sylph/plugins/pr-lifecycle/`, `agent-foundations/shared/conduct/verification.md`, `agent-foundations/shared/conduct/discipline.md`
- **Gap:** No standalone CM policy doc.

## CM-2 — Baseline Configuration
- **Status:** Implemented
- **Evidence:**
  - Plugin manifests (`<repo>/plugins/<plugin>/manifest.json`) declare versions.
  - `package.json` / `package-lock.json` pin npm deps.
  - `pyproject.toml` / `uv.lock` pin Python deps.
  - `.claude/settings.json` declares per-project hook + permission baseline.
- **Gap:** No single "system baseline" document; baseline distributed across repos.

## CM-2(2) — Automation Support
- **Status:** Implemented
- **Evidence:** Dependabot daily; lockfile-required convention; install.sh standardized.

## CM-2(3) — Retention of Previous Configurations
- **Status:** Implemented (git history)

## CM-2(7) — Configure Systems for High-Risk Areas
- **Status:** N/A (no travel/loaner-device program)

## CM-3 — Configuration Change Control
- **Status:** Implemented
- **Evidence:**
  - `sylph/plugins/pr-lifecycle/` enforces PR-based change.
  - `hydra/plugins/config-shield/` PreToolUse hook denies writes to security-sensitive config paths (`.claude/settings.json`, `egress-shield/config/`, hook scripts) without user confirmation.
  - `hydra/plugins/action-guard/` dry-run + confirm for destructive ops.
- **Gap:** No formal Change Control Board (single-maintainer today).

## CM-3(1) — Automated Documentation / Notification
- **Status:** Implemented
- **Evidence:** Every config change passes through git → PR → audit-trail.

## CM-3(2) — Test / Validate / Document Changes
- **Status:** Partial
- **Evidence:** `sylph/pr-lifecycle/` test-before-push gate; `agent-foundations/shared/scripts/` lint + verify.
- **Gap:** No regression-test matrix for hook scripts.

## CM-3(4) — Security Representative
- **Status:** Implemented (maintainer is also security owner)

## CM-4 — Impact Analyses
- **Status:** Partial
- **Evidence:** `lich/plugins/mantis-core/` code-review subagent inspects every PR; PR template includes "security impact" prompt.
- **Gap:** Impact-analysis is per-PR convention, not formal sign-off.

## CM-4(1) — Separate Test Environments
- **Status:** Partial
- **Evidence:** `lich/plugins/mantis-sandbox/` provides isolated execution for code review.
- **Gap:** No production-mirror staging environment (no hosted production exists).

## CM-5 — Access Restrictions for Change
- **Status:** Implemented
- **Evidence:**
  - GitHub branch protection on main: required reviews, signed commits, status checks.
  - `hydra/plugins/config-shield/` runtime block on security-sensitive paths.
- **Gap:** GitHub branch-protection settings not auditable from inside repo (must screenshot or query API).

## CM-5(1) — Automated Access Enforcement
- **Status:** Implemented (config-shield + branch protection)

## CM-5(5) — Privilege Limitation for Production
- **Status:** Planned (hosted)
- **Gap:** No hosted production yet.

## CM-6 — Configuration Settings
- **Status:** Implemented
- **Evidence:**
  - `.claude/settings.json` per project — permissions, hooks, env vars.
  - Per-plugin SKILL.md frontmatter — tool whitelist.
  - `hydra/plugins/egress-shield/config/allowlist.yaml` — egress baseline.
- **Gap:** No single "settings baseline" file across the ecosystem; per-project.

## CM-6(1) — Automated Management / Application / Verification
- **Status:** Partial
- **Evidence:** install.sh applies plugin settings; capability-fence verifies at runtime.
- **Gap:** No cross-plugin settings drift detection (depends on F-005 + naga/shift).

## CM-7 — Least Functionality
- **Status:** Implemented
- **Evidence:**
  - Per-plugin tool whitelist (smallest set principle from `skill-authoring.md`).
  - `hydra/plugins/capability-fence/` runtime enforcement.
  - `hydra/plugins/reach-filter/` limits skill discovery surface.

## CM-7(1) — Periodic Review
- **Status:** Partial
- **Evidence:** Quarterly compliance review; `wixie/plugins/inference-engine/` cross-session pattern detection on capability fires.

## CM-7(2) — Prevent Program Execution
- **Status:** Implemented
- **Evidence:** `hydra/plugins/capability-fence/` denies non-whitelisted tools; `hydra/plugins/action-guard/` denies destructive ops absent confirmation.

## CM-7(5) — Authorized Software / Allow-by-Exception
- **Status:** Implemented
- **Evidence:** `hydra/plugins/package-gate/` allowlists package names + version-range pins; typosquat detection.
- **Gap:** Allowlist completeness — see F-001 SBOM default-off.

## CM-8 — System Component Inventory
- **Status:** Implemented
- **Evidence:**
  - Plugin manifests + SKILL.md per skill.
  - `hydra/plugins/sbom-emitter/` generates CycloneDX SBOM on release.
- **Gap:** F-001 — SBOM default-off; needs default-on flip.

## CM-8(1) — Updates During Installation / Removal
- **Status:** Implemented (install.sh updates manifest)

## CM-8(3) — Automated Unauthorized Component Detection
- **Status:** Partial
- **Evidence:** `hydra/plugins/package-gate/` typosquat + allowlist; Dependabot novel-package alerts.
- **Gap:** Runtime unauthorized-binary detection absent.

## CM-9 — Configuration Management Plan
- **Status:** Partial
- **Evidence:** This document + `sylph/plugins/pr-lifecycle/` runbook.
- **Gap:** Not a standalone CM Plan artifact.

## CM-10 — Software Usage Restrictions
- **Status:** Partial
- **Evidence:** `hydra/plugins/license-gate/` checks dependency licenses against allowlist (MIT, Apache-2, BSD, etc.); blocks copyleft incompatibilities.
- **Gap:** No customer-facing EULA / usage restriction doc.

## CM-11 — User-Installed Software
- **Status:** Customer / Planned (hosted)

## CM-12 — Information Location
- **Status:** Implemented
- **Evidence:** `fedramp-boundary.md` § 4 documents where each information type lives.

---

## Family-level gaps (top 5)

1. **F-001** SBOM default-off — flip to default-on.
2. **F-002** No signed-artifact provenance (Sigstore/SLSA L3).
3. **No formal CM Plan artifact** — content exists, packaging doesn't.
4. **No regression-test matrix** for hook scripts (CM-3(2) partial).
5. **No cross-plugin settings drift detection** beyond Dependabot.
