# Annex A.3 — Internal organization

**Group:** A.3 — Internal organization
**Controls:** A.3.2, A.3.3
**Status:** Conformant.

## A.3.2 — AI roles and responsibilities

**Objective:** To establish accountability for AI systems within the organization.

**Control:** Roles and responsibilities for AI shall be defined and allocated according to the organization's needs.

**Implementation:**

Per `aims-policy.md` §5:

- **AI Owner** — project maintainer; signature authority on policy and reviews.
- **AI Custodian** — per-plugin lead per `plugin.json` `author` field.
- **AI Auditor** — reviewer-tier (Haiku) routine; external for cert-body engagement.
- **Incident Coordinator** — AI Owner (Critical); Custodian (plugin-scoped).

Per `wixie/CLAUDE.md`:

- Tier-level roles: Opus orchestrator, Sonnet executor, Haiku validator.
- Tier enforced via SKILL.md `model:` frontmatter field.

RACI summary in `aims-policy.md` §5.5.

**Evidence:**

- `aims-policy.md` §5
- `wixie/CLAUDE.md` § Agent tiers
- Per-plugin `plugin.json` files

**Conformance:** Full.

**Gap:** Some legacy plugins may lack `author` field. R-002.

---

## A.3.3 — Reporting of concerns

**Objective:** To provide a mechanism for raising concerns about AI systems.

**Control:** The organization shall define and put in place a process to report concerns about the organization's role with respect to an AI system, through appropriate channels.

**Implementation:**

Per `aims-policy.md` §10:

- **Routine nonconformity:** F-code logging in `learnings.md`.
- **Severity-High:** AI Custodian → AI Owner within 24h.
- **Severity-Critical:** Public advisory within 72h via GitHub Security Advisory.
- **Whistleblower / out-of-band:** GitHub Security Advisory or direct AI Owner contact; non-retaliation commitment.

**Evidence:**

- `aims-policy.md` §10
- GitHub Security Advisories on each repo
- `SECURITY.md` in repos (where present)

**Conformance:** Full.

**Gap:** Not all repos have explicit `SECURITY.md` pointing to advisory flow. R-016 (low priority).
