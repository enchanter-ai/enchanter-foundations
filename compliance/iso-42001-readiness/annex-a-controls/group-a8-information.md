# Annex A.8 — Information for interested parties of AI systems

**Group:** A.8 — Information for interested parties
**Controls:** A.8.2, A.8.3, A.8.4
**Status:** Conformant.

## A.8.2 — System documentation and information for users

**Control:** Documentation shall be made available to support intended users of AI systems.

**Implementation:**

- Per-plugin SKILL.md (description, preconditions, inputs, steps, outputs, handoff, failure modes).
- Per-plugin README.md (human-readable usage).
- Per-plugin `plugin.json` (machine-readable metadata).
- Per-skill frontmatter "Use when..." clause for discovery.
- Repository-level CLAUDE.md files for root-level conduct anchors.

**Evidence:**

- Per-plugin SKILL.md
- Per-plugin README.md
- Per-plugin `plugin.json`
- Repo CLAUDE.md files

**Conformance:** Full.

---

## A.8.3 — External reporting

**Control:** The organization shall report relevant information about the AI system to interested parties.

**Implementation:**

- `agent-foundations/compliance/` — public self-attestation for procurement / customer use.
- Quarterly self-re-attestation timestamp updated on each compliance map.
- GitHub Security Advisories for Severity-Critical issues.
- Public-by-default policy + conduct + compliance docs.

**Evidence:**

- `agent-foundations/compliance/iso-42001.md` (previous version)
- This readiness package
- GitHub Security Advisories (when issued)

**Conformance:** Full.

---

## A.8.4 — Communication of incidents

**Control:** Incidents shall be communicated to relevant parties.

**Implementation:**

Per `aims-policy.md` §10:

- Severity-Critical: public advisory within 72h of confirmation via GitHub Security Advisory.
- Severity-High: Custodian → Owner within 24h.
- Post-mortem authored within 14 days for High+.
- Cross-tenant Critical → public advisory within 30 days under self-imposed responsible-disclosure norm.

**Evidence:**

- `aims-policy.md` §10
- GitHub Security Advisory infrastructure on each repo

**Conformance:** Full at policy level. No actual incidents at attestation time (as of 2026-05-05).
