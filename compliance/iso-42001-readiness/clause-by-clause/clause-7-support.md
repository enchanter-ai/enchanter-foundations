# Clause 7 — Support

**ISO/IEC 42001:2023 §7**
**Status:** Self-attestation, conformant.
**Last reviewed:** 2026-05-05

## §7.1 Resources

### Requirement

The organization shall determine and provide the resources needed for the establishment, implementation, maintenance, and continual improvement of the AIMS.

### Resource categories

| Category | Provision |
|---|---|
| Time (maintainer hours) | Allocated per sprint per `wixie/prompts/security-closure/results/synthesis.md` |
| Compute (model tokens) | Per-tier budgeting via `shared/conduct/tier-sizing.md`; Haiku for mechanical, Sonnet for decomposed, Opus for intent |
| Cost watchdog | `pech/budget-watcher` tracks per-prompt cost |
| CI minutes | GitHub Actions; budgeted per repo |
| Storage | Per-plugin `state/` dirs; audit-trail log retention (default 24 months) |
| Tooling | Claude Code, MCP servers, vendor SDKs |
| Compliance maintenance | Quarterly self-re-attestation cycle |

### Evidence

- `shared/conduct/tier-sizing.md`
- `pech/budget-watcher/` SKILL.md
- `aims-policy.md` §1.3 (small-team scaling)

### Gap

None at clause level.

---

## §7.2 Competence

### Requirement

The organization shall determine the necessary competence of person(s) doing work that affects AI performance, ensure they are competent on the basis of education, training, or experience, take actions to acquire competence where needed, and retain documented information as evidence.

### Our position

"Competence" for AI agents (Claude tiers) is established by:

| Competence dimension | How established |
|---|---|
| Conduct module conformance | Loaded at session start; baked into reasoning |
| Tier-appropriate verbosity | `shared/conduct/tier-sizing.md` matches model to task density |
| Skill scope discipline | `shared/conduct/skill-authoring.md` enforces single-verb skills |
| Tool-use hygiene | `shared/conduct/tool-use.md` enforces right-tool-first-try |
| Verification discipline | `shared/conduct/verification.md` enforces independent checks |
| Failure-mode awareness | `shared/conduct/failure-modes.md` 14-code taxonomy |

For human contributors (the maintainer), competence is established by ongoing practice + the same conduct modules as guidance.

### Continuous training

- Inference-engine briefings serve as "training material" delivered at session start.
- `learnings.md` per workflow accumulates lessons across iterations.
- Precedent log accumulates operational gotchas.

### Evidence

- `shared/conduct/*.md` (all modules)
- `wixie/plugins/inference-engine/state/briefings/<plugin>.md`
- Per-plugin `learnings.md`
- Per-project `state/precedent-log.md`

### Gap

None at clause level. The "competence" framing maps awkwardly to AI agents — we substitute conduct-module conformance as the analogue and document it.

---

## §7.3 Awareness

### Requirement

Person(s) doing work under the organization's control shall be aware of:

- the AI policy;
- their contribution to AIMS effectiveness;
- the implications of nonconformity.

### Our position

| Awareness target | Mechanism |
|---|---|
| AI policy | `aims-policy.md` referenced from root `CLAUDE.md` files |
| Conduct modules | Loaded at session start via `@shared/conduct/*.md` references |
| Per-plugin briefings | Inference-engine renders briefing to `state/briefings/<plugin>.md`; read at session start |
| Contribution to effectiveness | Lifecycle skills are *the* contribution; success criteria explicit in DEPLOY bar |
| Implications of nonconformity | F-code logging required; revert-on-regression auto-enforced; precedent log surfaces recurring gotchas |

### Communication of awareness

- Top-200-tokens U-curve slot (per `shared/conduct/context.md`) used for the most important reminders.
- Conduct modules use second-person imperative ("YOU MUST", "NEVER") to bias attention.

### Evidence

- Root `CLAUDE.md` references to `@shared/conduct/*.md`
- `shared/conduct/context.md` § U-curve placement
- `wixie/plugins/inference-engine/state/briefings/`

### Gap

None at clause level.

---

## §7.4 Communication

### Requirement

The organization shall determine the internal and external communications relevant to the AIMS, including:

- on what to communicate;
- when;
- with whom;
- how;
- who communicates.

### Internal communication

| What | When | With whom | How | Who |
|---|---|---|---|---|
| Conduct modules | Session start | Active agent | `@shared/conduct/*.md` references | Auto via CLAUDE.md |
| Inference-engine briefings | Session start | Active agent | `state/briefings/<plugin>.md` | Engine + skill |
| Reviewer feedback | Per iteration | Crafter / refiner | In-session reply | Reviewer-tier (Haiku) |
| Convergence verdict | Per round | Operator | Skill reply + `learnings.md` | Convergence engine |
| Audit-trail events | Real-time | Operator | `state/log.jsonl` | Hydra audit-trail |

### External communication

| What | When | With whom | How | Who |
|---|---|---|---|---|
| Compliance attestations | Quarterly + on-change | Procurement / customers | This folder, public repo | AI Owner |
| Severity-Critical advisories | Within 72h of confirmation | Public | GitHub Security Advisory | AI Owner |
| Conduct-module updates | On merge | Open-source community | Git commit + changelog | Contributor + AI Owner |
| Policy version bump | On material change | Interested parties | Public repo + signed re-attestation | AI Owner |

### Evidence

- This folder + sibling compliance maps
- `hydra/audit-trail/`
- GitHub Security Advisories (when issued)

### Gap

- No formal mailing list / RSS for compliance updates. Acceptable; interested parties follow the repo.

---

## §7.5 Documented information

### §7.5.1 General

#### Requirement

The AIMS shall include documented information required by ISO 42001 and that the organization determines necessary for AIMS effectiveness.

#### Our documented information

Per `aims-policy.md` §7.1 hierarchy:

```
AIMS Policy (apex)
├── Compliance maps (this folder + siblings)
├── Conduct modules (shared/conduct/*.md)
├── Skill catalogs (per-plugin SKILL.md)
├── Risk register
└── Operational artifacts
    ├── learnings.md per workflow
    ├── precedent-log.md per project
    ├── inference-engine/state/artifacts.jsonl
    └── audit-trail/state/log.jsonl
```

---

### §7.5.2 Creating and updating

#### Requirement

Documented information shall be appropriately identified, formatted, reviewed, and approved.

#### Our practice

| Aspect | Practice |
|---|---|
| Identification | File path + git-tracked version + frontmatter where applicable |
| Format | Markdown for human-readable; JSON / JSONL for machine-readable; YAML for frontmatter |
| Review | PR review for material changes; reviewer-tier (Haiku) for routine |
| Approval | AI Owner for material; Custodian for routine |

#### Evidence

- Git history across repos
- PR comments + reviews
- `shared/conduct/skill-authoring.md` frontmatter discipline

---

### §7.5.3 Control of documented information

#### Requirement

Documented information shall be available and suitable for use where and when needed, and shall be adequately protected (confidentiality, integrity, availability).

#### Our practice

| Concern | Practice |
|---|---|
| Availability | Open-source repos; per-operator local copies |
| Suitability for use | Conduct modules are auto-loaded; briefings auto-rendered; SKILL.md is loaded by Claude Code |
| Confidentiality | Public policy + conduct; operator-private audit logs + risk registers |
| Integrity | Git history; HMAC chain on audit log; SHA-1 fingerprints on inference-engine artifacts |
| Storage | Git for tracked docs; per-plugin `state/` for runtime artifacts; operator-private storage for signed copies |
| Retention | Git history indefinite; audit log 24mo default; inference-engine artifacts indefinite |
| Disposition | Resolved entries marked `RESOLVED YYYY-MM-DD` in precedent log; retired patterns in inference-engine retain LLR history |

#### Access control

- Public-by-default for policy + conduct + compliance maps.
- Operator-private for risk register details, audit logs, signed commitment statements.
- No documents are write-restricted via runtime ACL; protection is via git review + branch protection on `main`.

#### Evidence

- `.gitignore` patterns (operator-private dirs)
- Branch protection on main branches
- HMAC verification on audit log

#### Gap

- HMAC key rotation procedure not formally documented. Tracked R-013.
