# Annex A.10 — Third-party and customer relationships

**Group:** A.10 — Third-party and customer relationships
**Controls:** A.10.2, A.10.3, A.10.4
**Status:** Conformant with supply-chain gap.

## A.10.2 — Allocating responsibilities

**Control:** Responsibilities between the organization and third-party providers / customers shall be allocated.

**Implementation:**

- AIMS scope (`aims-policy.md` §2) explicitly delineates what is our responsibility vs. vendor (Claude, GPT, Gemini API providers) vs. downstream operator.
- Third-party AI products consumed: vendor governs; we comply with vendor TOS.
- Customer agents built atop our skills: downstream operator's AIMS governs.
- Our AIMS: the skills, conduct, runtime guardrails, audit trail.

**Supply-chain controls:**

- `hydra/sbom-emitter` (default-off — F-001 gap).
- `hydra/license-gate` (shipped; `--fail-on-deny` not wired into release.yml — F-014 partial).
- `hydra/package-gate` (typosquat detection; seed list refresh F-023 gap).
- Dependabot config (shipped).
- OSV-Scanner cron (F-009 partial).
- Sigstore + SLSA L3 (F-002 gap — MUST-SHIP queue).

**Evidence:**

- `aims-policy.md` §2 (scope)
- `hydra/sbom-emitter/`, `hydra/license-gate/`, `hydra/package-gate/`
- `wixie/prompts/security-closure/results/synthesis.md`

**Conformance:** Conformant at policy level; supply-chain controls partial (MUST-SHIP queue active).

**Gap:**

- F-001 SBOM default-off — R-003.
- F-002 Sigstore + SLSA L3 missing — R-004.
- F-014 license-gate `--fail-on-deny` not wired — R-011.

---

## A.10.3 — Suppliers

**Control:** Relationships with suppliers shall be managed.

**Implementation:**

- Vendor relationships: Claude (Anthropic), GPT (OpenAI), Gemini (Google) — governed by vendor TOS.
- Tooling: Claude Code, GitHub, MCP servers — governed by respective TOS.
- Open-source dependencies: managed via Dependabot + license-gate + package-gate.
- No managed-service AI providers beyond inference APIs.

**Evidence:**

- `package.json` / `pyproject.toml` per repo (dependency manifests)
- `hydra/license-gate/` allowed-license list
- Dependabot configs

**Conformance:** Conformant. Vendor compliance is implicit; we do not contract-audit Anthropic/OpenAI/Google.

---

## A.10.4 — Customers

**Control:** Customer relationships shall be managed.

**Implementation:**

- Public-by-default compliance documents support customer / procurement due diligence.
- This readiness package + sibling maps (`nist-ai-rmf.md`, `soc2.md`, `fedramp-boundary.md`) serve as the customer-facing artifact set.
- GitHub Issues / Security Advisories serve as the customer feedback / incident channel.

**Evidence:**

- `agent-foundations/compliance/`
- GitHub Issues + Security Advisories

**Conformance:** Conformant.

**Gap:** No formal customer SLA or contract template for enterprise procurement. Acceptable for open-source scale; revisit if commercial offerings emerge.
