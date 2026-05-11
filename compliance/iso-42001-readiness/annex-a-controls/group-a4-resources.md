# Annex A.4 — Resources for AI systems

**Group:** A.4 — Resources for AI systems
**Controls:** A.4.2, A.4.3, A.4.4, A.4.5, A.4.6
**Status:** Conformant.

## A.4.2 — Resource documentation

**Objective:** To document the resources required for the AI system.

**Control:** The organization shall identify and document relevant resources required for the AI system activities, including subservices.

**Implementation:**

- Per-tier model assignments documented in `wixie/CLAUDE.md` § Agent tiers.
- Per-plugin resource notes in `SKILL.md` files.
- `pech/budget-watcher` tracks token + cost per workflow.
- `shared/conduct/tier-sizing.md` documents resource allocation by task density.

**Evidence:**

- `wixie/CLAUDE.md`
- Per-plugin `SKILL.md`
- `pech/budget-watcher/SKILL.md`

**Conformance:** Full.

---

## A.4.3 — Data resources

**Objective:** To document data resources used by AI systems.

**Control:** Data resources used for AI system development and operation shall be documented.

**Implementation:**

- `shared/conduct/web-fetch.md` cite hygiene — every fetched fact has `url`, `date`, `source_type`, `quote`.
- `wixie/deep-research` outputs `claims.json` + `sources.jsonl` per brief.
- Brief retention with 30-day freshness threshold for reuse.
- `<untrusted_source>` wrapping segregates external data from instruction context.

**Evidence:**

- `shared/conduct/web-fetch.md`
- `wixie/plugins/deep-research/state/briefs/<slug>/`
- `wixie/CLAUDE.md` § Engines § E0 Deep Research

**Conformance:** Full.

---

## A.4.4 — Tooling resources

**Objective:** To document tooling resources used by AI systems.

**Control:** Tooling resources used for AI system development and operation shall be documented.

**Implementation:**

- Per-skill `tools:` whitelist in SKILL.md frontmatter (per `shared/conduct/skill-authoring.md`).
- `shared/conduct/tool-use.md` enforces right-tool-first-try.
- `shared/conduct/delegation.md` enforces minimal tool whitelist per subagent role.

**Evidence:**

- Per-plugin SKILL.md frontmatter `tools:` field
- `shared/conduct/tool-use.md`
- `shared/conduct/delegation.md`

**Conformance:** Full.

---

## A.4.5 — System and computing resources

**Objective:** To document compute resources.

**Control:** System and computing resources used for AI system development and operation shall be documented.

**Implementation:**

- Workstation-based execution (developer machines).
- GitHub Actions CI runners for cross-repo workflows.
- `pech/budget-watcher` tracks per-prompt cost (cost ≈ compute).
- No on-prem infrastructure; no managed services beyond GitHub + vendor APIs.

**Evidence:**

- `pech/budget-watcher/`
- `.github/workflows/` per repo
- `aims-policy.md` §2.3 (out-of-scope: physical infrastructure)

**Conformance:** Full.

---

## A.4.6 — Human resources

**Objective:** To document human resources required for AI systems.

**Control:** Human resources required for the AI system activities shall be documented.

**Implementation:**

- AI Owner, Custodian, Auditor, Coordinator roles in `aims-policy.md` §5.
- Skill-level tier assignment (Opus/Sonnet/Haiku) functions as "AI human-equivalent role".
- For human operators: the developer running Claude Code with our skills is the documented human role per downstream operator's own AIMS.

**Evidence:**

- `aims-policy.md` §5
- Per-plugin `plugin.json` `author` field

**Conformance:** Full.
