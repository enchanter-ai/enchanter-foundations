# Annex A.7 — Data for AI systems

**Group:** A.7 — Data for AI systems
**Controls:** A.7.2, A.7.3, A.7.4, A.7.5, A.7.6
**Status:** Conformant.

## A.7.2 — Data for development and enhancement of AI systems

**Control:** Data for development and enhancement of AI systems shall meet requirements.

**Implementation:**

- We do not train models (out of scope per `aims-policy.md` §2.3).
- Data for *prompt development* comes from `/deep-research` outputs, which apply cite hygiene per `shared/conduct/web-fetch.md`.
- `claims.json`, `sources.jsonl`, `trace.json` per brief.

**Evidence:** `wixie/plugins/deep-research/state/briefs/`; `shared/conduct/web-fetch.md`.

**Conformance:** Full.

---

## A.7.3 — Acquisition of data

**Control:** Data acquisition shall be controlled.

**Implementation:**

- `/deep-research` fetcher subagents (Haiku-tier per `shared/conduct/web-fetch.md`) own all `WebFetch` calls.
- URL-hash cache (24h TTL); query-hash cache for `WebSearch`.
- Budget discipline: 200 KB session-wide, 400 words per fetcher output, 8 KB per page extracted text (with `partial: true` flag on truncate).

**Evidence:** `shared/conduct/web-fetch.md`; `wixie/plugins/deep-research/agents/fetcher.md`.

**Conformance:** Full.

---

## A.7.4 — Quality of data for AI systems

**Control:** Quality of data shall be assured.

**Implementation:**

- Cite hygiene fields enforced: `url`, `date`, `source_type`, `quote` (verbatim ≤200 chars).
- Paraphrase-as-quote → F02 (Fabrication) — flagged + rejected.
- Topic filter applied *before* extraction (per `shared/conduct/web-fetch.md` § Failure modes F13 counter).
- `source_type` taxonomy: `official | third-party | community | paper | other`.

**Evidence:** `shared/conduct/web-fetch.md`; `wixie/plugins/deep-research/agents/fetcher.md`.

**Conformance:** Full.

---

## A.7.5 — Data provenance

**Control:** Data provenance shall be recorded.

**Implementation:**

- Every fetched fact carries: `url`, `date` (or null), `source_type`, `quote`.
- `<untrusted_source>` wrapping segregates external data from instruction context.
- Brief retention preserves provenance for reuse (30-day freshness threshold).

**Evidence:** `wixie/plugins/deep-research/state/briefs/<slug>/sources.jsonl`; `shared/conduct/web-fetch.md`.

**Conformance:** Full.

---

## A.7.6 — Data preparation

**Control:** Data preparation shall be performed.

**Implementation:**

- `<untrusted_source>` XML wrapping in deep-research outputs prevents prompt-injection escalation when external data flows into downstream prompts.
- Topic-filter test (per fetcher senior-to-junior prompt) excludes adjacent topics.
- Claim test + quote test ensure data quality before recording.

**Evidence:** `wixie/plugins/deep-research/agents/fetcher.md`; `shared/conduct/web-fetch.md`.

**Conformance:** Full.
