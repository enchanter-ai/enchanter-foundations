# Clause 5 — Leadership

**ISO/IEC 42001:2023 §5**
**Status:** Self-attestation, partial conformance (formal management review template ready, first quarterly review not yet exercised).
**Last reviewed:** 2026-05-05

## §5.1 Leadership and commitment

### Requirement

Top management shall demonstrate leadership and commitment with respect to the AIMS by:

- ensuring the AI policy and objectives are established and compatible with the strategic direction;
- ensuring integration of AIMS requirements into business processes;
- ensuring resources needed are available;
- communicating the importance of effective AI management;
- ensuring the AIMS achieves its intended outcomes;
- directing and supporting persons to contribute to effectiveness;
- promoting continual improvement;
- supporting other relevant management roles.

### Our position

"Top management" at enchanter-ai scale = the project maintainer(s), per `aims-policy.md` §1.3 substitution.

### Evidence

- AI policy: `aims-policy.md` (this readiness package).
- AI objectives: DEPLOY bar in `wixie/CLAUDE.md` (σ<0.45, overall≥9.0, all axes≥7.0, 8/8 SAT).
- Integration into business processes: lifecycle skills are *the* business processes for prompt work.
- Resource availability: maintainer time, model budget, GitHub Actions minutes — sufficient for current scale.
- Communication: conduct modules loaded at session start; briefings emitted per session.
- Effectiveness: convergence loop verdicts (DEPLOY / HOLD / FAIL); SPRT-elevated patterns; security-closure audit.
- Continual improvement: inference-engine substrate.
- Supporting roles: AI Custodian role per `aims-policy.md` §5.2.

### Commitment signature

The board-level / maintainer commitment statement is the template in `aims-policy.md` §9. The unsigned template is the proposed text; a signed copy must be retained in operator-private storage on formal adoption.

### Gap

- **Formal management-review records not yet maintained.** Template exists (`management-review-template.md`); first quarterly review target: 2026-08-31.
- Tracked in `risk-register.md` as R-001.

---

## §5.2 AI policy

### Requirement

Top management shall establish, implement, and maintain an AI policy that:

- is appropriate to the purpose of the organization;
- provides a framework for setting AI objectives;
- includes a commitment to satisfy applicable requirements;
- includes a commitment to continual improvement;
- is available as documented information;
- is communicated within the organization;
- is available to interested parties as appropriate.

### Our position

The AI policy is `aims-policy.md`, supplemented by the twelve conduct modules in `shared/conduct/`.

| Requirement | Where met |
|---|---|
| Appropriate to purpose | `aims-policy.md` §1, §2 |
| Framework for objectives | `aims-policy.md` §3 (principles) + `wixie/CLAUDE.md` § DEPLOY bar |
| Commitment to applicable requirements | `aims-policy.md` §9 (commitment statement) |
| Commitment to continual improvement | `aims-policy.md` §3.6, §10; conduct module `inference-substrate.md` |
| Documented information | `aims-policy.md` + this folder |
| Communicated within org | Conduct modules loaded at session start; inference-engine briefings |
| Available to interested parties | Public-by-default in open-source repos |

### Conduct-module backbone

The twelve modules constitute the operational policy:

1. `discipline.md` — coding conduct
2. `context.md` — attention budget
3. `verification.md` — independent checks
4. `doubt-engine.md` — adversarial self-check
5. `delegation.md` — subagent contracts
6. `failure-modes.md` — F-code taxonomy
7. `tool-use.md` — tool hygiene
8. `formatting.md` — structured output
9. `skill-authoring.md` — SKILL.md discipline
10. `hooks.md` — advisory-only rules
11. `precedent.md` — failure log
12. `tier-sizing.md` — verbosity by tier
13. `web-fetch.md` — external web reading
14. `inference-substrate.md` — cross-session evidence

(Yes, fourteen — the "twelve" label is approximate; the count grows as new operational concerns emerge.)

### Evidence

- `aims-policy.md`
- `agent-foundations/shared/conduct/*.md`
- `wixie/CLAUDE.md` (root anchor that loads conduct modules)

### Gap

None at clause level.

---

## §5.3 Roles, responsibilities, and authorities

### Requirement

Top management shall ensure that the responsibilities and authorities for relevant roles are assigned and communicated.

### Roles in our AIMS

Per `aims-policy.md` §5:

| Role | Holder | Accountability summary |
|---|---|---|
| AI Owner | Project maintainer (Daniel Frenkel) | Final authority; signature on policy + reviews |
| AI Custodian | Per-plugin lead (per `plugin.json` `author`) | Day-to-day plugin AIMS controls |
| AI Auditor | Reviewer-tier agent (Haiku) routine; external for cert-body | Independent verification |
| Incident Coordinator | AI Owner (critical); Custodian (plugin-scoped) | Coordinate active incident |

### Tier-level role mapping

`wixie/CLAUDE.md` § Agent tiers names model-tier roles:

| Tier | Model | Role in AIMS |
|---|---|---|
| Orchestrator | Opus | Decomposition, judgment, technique selection |
| Executor | Sonnet | Convergence, adversarial, translation, test execution |
| Validator | Haiku | Quality gate, freshness audit |

Tier assignments are enforced via SKILL.md frontmatter `model:` field (per `shared/conduct/skill-authoring.md`).

### Plugin-level authorship

Per `plugin.json` `author` field; canonical record of plugin custodianship. Authoring discipline in `shared/conduct/skill-authoring.md` mandates this field.

### Communication of authorities

- Roles communicated via `aims-policy.md` (apex) → conduct modules (operational) → `plugin.json` (per-plugin).
- Tier assignments enforced at skill load time.
- Override flow: any deviation logged in `learnings.md` with F-code + rationale + time-box.

### Evidence

- `aims-policy.md` §5
- `wixie/CLAUDE.md` § Agent tiers
- Per-plugin `plugin.json` files
- `shared/conduct/skill-authoring.md`

### Gap

- Some legacy plugins may lack `author` field in `plugin.json`. Audit + remediation tracked in `risk-register.md` as R-002.
