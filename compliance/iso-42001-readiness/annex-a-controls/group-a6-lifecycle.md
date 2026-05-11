# Annex A.6 — AI system lifecycle

**Group:** A.6 — AI system lifecycle
**Controls:** A.6.1.2, A.6.1.3, A.6.1.4, A.6.2.2, A.6.2.3, A.6.2.4, A.6.2.5, A.6.2.6, A.6.2.7, A.6.2.8
**Status:** Conformant with multiple roadmap items.

## A.6.1.2 — Objectives for responsible development of AI systems

**Control:** The organization shall identify and document objectives to guide the responsible development of AI systems.

**Implementation:**

- DEPLOY bar: σ<0.45, overall≥9.0, all 5 axes≥7.0, 8/8 SAT (`wixie/CLAUDE.md`).
- AI principles in `aims-policy.md` §3 (fairness, accountability, transparency, safety, privacy, robustness, sustainability).
- No-regression contract enforced by convergence engine.

**Evidence:** `wixie/CLAUDE.md` § DEPLOY bar; `aims-policy.md` §3; `wixie/convergence-engine/`.

**Conformance:** Full.

---

## A.6.1.3 — Processes for the responsible development of AI systems

**Control:** Processes for responsible development shall be defined.

**Implementation:** Lifecycle skills: `/deep-research` → `/create` → `/refine` → `/converge` → `/test-prompt` → `/harden` → `/translate-prompt`. Each is a skill with explicit preconditions, inputs, steps, outputs, handoff (per `shared/conduct/skill-authoring.md`).

**Evidence:** `wixie/CLAUDE.md` § Lifecycle; per-skill SKILL.md.

**Conformance:** Full.

---

## A.6.1.4 — Acquired AI systems

**Control:** Where AI systems are acquired (e.g., from third-party providers), the organization shall ensure they meet relevant requirements.

**Implementation:** AIMS scope explicitly excludes third-party AI consumed (Claude, GPT, Gemini APIs) — vendor governance applies. We document the vendor TOS dependency implicitly.

**Evidence:** `aims-policy.md` §2.3 (out-of-scope).

**Conformance:** N/A explicit — out of scope by design. Documented.

---

## A.6.2.2 — AI system requirements and specification

**Control:** Requirements for an AI system shall be specified.

**Implementation:**

- Per-prompt success criterion stated in `learnings.md` or via the lifecycle skill input.
- DEPLOY bar acts as universal acceptance threshold.
- Per-target model formatting requirements per `shared/conduct/formatting.md`.

**Evidence:** Per-prompt `learnings.md`, `metadata.json`.

**Conformance:** Full.

---

## A.6.2.3 — Documentation of AI system design and development

**Control:** AI system design and development shall be documented.

**Implementation:**

- Per-prompt folder: `prompt.<ext>`, `metadata.json`, `tests.json`, `report.pdf`, `learnings.md`.
- Per-plugin SKILL.md describes design.
- Per-plugin `plugin.json` records authorship + scope.

**Evidence:** `wixie/prompts/`; per-plugin SKILL.md.

**Conformance:** Full.

---

## A.6.2.4 — Verification and validation

**Control:** AI systems shall be verified and validated.

**Implementation:**

- `wixie/prompt-tester` regression suite: ≥3 cases, ≥1 edge-case.
- `shared/conduct/verification.md` three-mode verification: tier split (Haiku reviewer), deterministic check (test/lint/hash), diff read-back (fresh agent on diff).
- DEPLOY bar acts as numeric validation threshold.

**Evidence:** Per-prompt `tests.json`; `shared/conduct/verification.md`.

**Conformance:** Full.

---

## A.6.2.5 — Deployment

**Control:** Deployment shall follow defined processes.

**Implementation:**

- `/translate-prompt --to <model>` for cross-target deployment with score comparison.
- Deployment artifacts: per-target `prompt.<ext>` + comparison metadata.
- Format-follows-model rule per `shared/conduct/formatting.md` (XML for Claude, sandwich for GPT, minimal for o-series, few-shot for Gemini).

**Evidence:** `wixie/prompt-translate/`; `shared/conduct/formatting.md`.

**Conformance:** Full.

---

## A.6.2.6 — AI system operation and monitoring

**Control:** AI systems in operation shall be monitored.

**Implementation:**

- `hydra/audit-trail/state/log.jsonl` (HMAC-chained, real-time).
- `naga/naga-observe` drift events.
- `wixie/inference-engine` cross-session pattern accumulation.
- Per-prompt `learnings.md` records iteration outcomes.

**Evidence:** `hydra/plugins/audit-trail/`; `wixie/plugins/inference-engine/`.

**Conformance:** Full at log-level; gap at OTLP-grade observability.

**Gap:** OTLP / Sentry / Datadog span exporter not yet shipped. F-021/F-024. R-005.

---

## A.6.2.7 — Technical documentation

**Control:** Technical documentation shall be produced.

**Implementation:**

- Per-plugin SKILL.md (runbook structure: preconditions, inputs, steps, outputs, handoff, failure modes).
- Per-plugin `plugin.json` (machine-readable metadata).
- Conduct modules (cross-cutting behavioral docs).
- Compliance maps (this folder + siblings).
- Per-prompt `report.pdf` (dark-themed single-page audit).

**Evidence:** SKILL.md, plugin.json, conduct modules, compliance maps.

**Conformance:** Full.

---

## A.6.2.8 — AI system recording of event logs

**Control:** Event logs shall be recorded and retained.

**Implementation:**

- `hydra/plugins/audit-trail/state/log.jsonl` HMAC-chained.
- 24-month default retention per `aims-policy.md` §7.3.
- Operator-configurable extension for longer retention.

**Evidence:** `hydra/plugins/audit-trail/`; `aims-policy.md` §7.3.

**Conformance:** Full.

**Gap:** HMAC key rotation procedure not formally documented. R-013.
