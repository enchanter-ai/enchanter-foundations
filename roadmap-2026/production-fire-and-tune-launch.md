# Production Fire-and-Tune Launch — Operator Package

**Status:** Draft v1 — operator runbook
**Owner:** Vis (security + DX)
**Upstream artifact:** `security/synthetic-fire-2026-05/` (synthetic harness, regression baseline, gap analysis)
**Downstream gate:** General Availability (GA) launch
**Target window:** 16 weeks (3 cohorts, weeks 1-16+)

---

## 0. Why this document exists

The synthetic harness at `security/synthetic-fire-2026-05/` proved the shields *can* fire correctly against curated attack corpora. It does not prove they fire correctly against the *long tail* of real customer traffic. Per `security/synthetic-fire-2026-05/external-real-traffic-gap.md`, the gap is:

- Synthetic FP/FN rates are measured against attacks we wrote. Real attacks are written by people who haven't read our threat model.
- Synthetic latency is measured on idle hardware. Real latency competes with the customer's actual workload.
- "Novel attack surfaces" cannot be measured without an external surface.

The fire-and-tune phase closes the gap by routing real traffic through advisory-mode shields, collecting telemetry, tuning thresholds, and graduating to blocking mode only after the FP rate proves harmless.

This document is the operator playbook — recruitment, structure, telemetry, privacy, tuning, exit criteria, GA, and what we tell design partners. It is not code. It is the sales motion plus the measurement contract that lets us ship blocking shields without breaking customer builds.

---

## 1. Design-partner recruitment plan

### 1.1 Target profile

We are looking for customers who match all four:

| Trait | Concrete signal |
|-------|-----------------|
| AI-native dev team | At least one production agent loop (Claude Code, Cursor agent mode, internal Bedrock/Vertex agent), not just chat completion |
| Security-conscious | Has a security review process; has at least one engineer who reads the threat model before approving deps |
| Mid-size | 10-50 engineers — large enough that an incident matters, small enough to ship a config change without a 6-week change-board cycle |
| Friction-tolerant | Willing to file a Slack message when a shield trips falsely, instead of disabling and ghosting |

We are explicitly *not* targeting Fortune 500 in this phase. Enterprise procurement cycles dominate the engineering signal we need.

### 1.2 Recruitment channels (in priority order)

1. **Direct outreach to existing personal network.** 8-12 founder/principal-engineer contacts running AI-native teams. Highest signal, fastest response, lowest acquisition cost. Target: 3 closed in first 2 weeks.
2. **HN Show post.** "Show HN: We built shields for agent runtimes — looking for 5 design partners to test against real traffic." Publish in week 1; expect 1-2 qualified leads.
3. **Discord communities.** Anthropic API users, OpenAI dev community, LangChain, Cursor power-users channels. Soft pitch in #show-and-tell channels; do not cold-DM moderators.
4. **Targeted X/Twitter posts** from founder/principals accounts. One thread describing the synthetic harness results + invitation to apply. No paid amplification.
5. **Conference side-channel.** If a relevant security/AI-engineering event lands in the window, attend; do not sponsor.

Channels deliberately excluded: paid ads (signal-to-noise too poor at this stage), LinkedIn InMail spam (kills the brand), Reddit (audience mismatch for B2B security tooling).

### 1.3 Incentive structure

| Cohort | What they get | What we ask |
|--------|---------------|-------------|
| Cohort A (weeks 1-4) | 6 months free post-GA + named in launch post if they consent + monthly co-design session with founders | Telemetry opt-in, weekly 30-min check-in, NDA-light (mutual non-disparagement, no IP exchange) |
| Cohort B (weeks 5-12) | 3 months free post-GA + design input on capability-fence + audit-trail features | Same telemetry, biweekly check-in, NDA-light |
| Cohort C (weeks 13+) | 1 month free post-GA + first access to GA tier | Telemetry opt-in only; no required check-ins |

We do not pay design partners and we do not give equity. Cash incentives select for the wrong customer profile. Free credit selects for customers who actually use the product.

### 1.4 NDA-light scope

The legal surface is intentionally minimal:

- **Mutual non-disparagement** during the pilot.
- **Confidentiality on shield internals** — they don't publish our detection heuristics; we don't publish their attack traces without consent.
- **No IP transfer in either direction.**
- **Either party may exit with 7 days notice** — no clawback, no penalty.

A standard MNDA, signed via Docusign in under 10 minutes. If a prospect requests a 4-week legal review for the pilot itself, they are the wrong cohort.

---

## 2. Pilot program structure

Three cohorts, staged. Each cohort gates on the previous one's exit criteria.

### 2.1 Cohort A — Advisory-only baseline (weeks 1-4)

**Size:** 3-5 customers.
**Shields enabled:** canary (advisory), package-gate (advisory), egress-monitor (advisory).
**Mode:** *Advisory* — every detection logs an event, no detection blocks an action.
**Goal:** Baseline FP rate per shield against real traffic. Quantify the gap between the synthetic baseline and reality.

What "advisory" means concretely:
- Shield fires its detection logic on every relevant tool call.
- Detection writes an event to the customer's local audit log + (with consent) ships an anonymized summary to our telemetry endpoint.
- Action proceeds regardless of detection verdict.
- Customer sees a one-line "advisory" indicator in their IDE/CLI showing "shield X flagged this — review later".

Cohort A succeeds when we have ≥ 2 weeks of telemetry per customer and per-shield FP rate is calculable to ±2 percentage points.

### 2.2 Cohort B — Expanded shield set (weeks 5-12)

**Size:** 5-10 customers (Cohort A continues; new customers added).
**Shields enabled:** Cohort A set + capability-fence (advisory), audit-trail HMAC (active, no UX impact), OTLP export (active for customers with existing observability stack).
**Mode:** Cohort A shields graduate to *block-on-high-confidence* if Cohort A FP rate ≤ 5%; otherwise stay advisory. New shields enter advisory-only.
**Goal:** Validate tuning fixes from Cohort A, measure FP rate for capability-fence (the highest-FP-risk shield), validate OTLP export interoperability with Datadog/Honeycomb/Grafana.

### 2.3 Cohort C — Full opt-in blocking (weeks 13+)

**Size:** 10+ customers.
**Shields enabled:** All seven shields available; customer opts into blocking mode per shield via config.
**Mode:** Blocking is *opt-in only*. Default remains advisory until customer flips the flag.
**Goal:** Demonstrate that ≥ 60% of Cohort C customers choose to opt at least three shields into blocking within 4 weeks. If they don't, the shields aren't trusted yet — return to tuning.

---

## 3. Telemetry collection checklist

### 3.1 What we capture

Per shield-firing event:

- **Timestamp** (UTC, second precision).
- **Shield name + version** (e.g., `canary@1.4.2`).
- **Verdict** (`block | warn | allow`).
- **Confidence score** (0.0-1.0 if the shield emits one).
- **Latency** (microseconds from invocation to verdict).
- **Tool name being intercepted** (e.g., `Bash`, `Write`, `WebFetch`) — not the args.
- **Trigger pattern category** (e.g., `package-gate:typosquat`, `egress-monitor:unknown-domain`) — categorical, not the raw match.
- **Customer ID** (opaque UUID assigned at pilot start; not derivable from anything the customer types).
- **Session ID** (opaque, per-conversation; rotates).

Per pilot week (aggregated locally first, then shipped):

- Total tool calls intercepted, by tool type.
- Total shield events, by shield + verdict.
- Customer-flagged FPs (a button in the IDE indicator: "this wasn't actually malicious").
- Customer-flagged FNs (out-of-band Slack: "shield missed this attack on us").
- p50, p95, p99 shield latency.
- Novel attack pattern surfaces (we'll define these via Cohort A; initial proxies: `confidence > 0.95 on a never-before-categorized pattern`).

### 3.2 What we do not capture

Hard rules — these never leave the customer's machine:

- **Source code.** Not file contents, not snippets, not even file paths beyond the basename's category.
- **Secrets.** Not env vars, not API keys, not tokens — even when redacted by a shield, the redacted form stays local.
- **PII.** Not user names, not emails, not IPs of the customer's developers. Customer ID is the only identity tracked.
- **Prompt contents.** Not the user prompt to the agent, not the agent's response, not the tool args. Only categorical metadata.
- **Network destinations beyond category.** A blocked egress event records `category: unknown-external` not `host: evil.example.com`.

The customer can read every byte we ship by tailing the local audit log. There are no hidden channels.

### 3.3 Transport + storage

- Telemetry batched locally, shipped every 15 minutes over TLS to a single endpoint (`telemetry.vis.dev`, IP-pinned in shield config).
- Endpoint writes to an append-only object store (S3 with object-lock at-rest), 90-day TTL.
- After 90 days, raw events are aggregated to weekly summaries (FP rate per shield, per cohort) and raw events deleted.
- Aggregated summaries retained indefinitely for cross-cohort comparison.

---

## 4. Privacy + data-handling stance

### 4.1 Principles

1. **Opt-in only.** Telemetry is disabled by default. Customer flips a single config flag to enable. Disabling mid-pilot is fine; we keep the data already shipped, customer can request deletion (§ 4.3).
2. **Local aggregation before transit.** Where feasible, the shield aggregates locally (per-15-min counts) and ships the aggregate, not raw events. Per-event ship is reserved for FP-flag and novel-pattern surfaces.
3. **Anonymization at the boundary.** The shipping client strips any field that could be a covert channel — long strings, base64-looking blobs, hostnames. The receiving endpoint validates schema before write.
4. **Retention 90 days then aggregated-only.** Raw event-level data is destroyed at day 90. Aggregated counts persist.
5. **Customer right to delete on request.** A `/delete` endpoint accepting the customer ID + a signed token (from the customer's pilot config) wipes all event-level data for that customer within 30 days. Aggregated summaries that already incorporated their data remain (we cannot un-bake a cookie) but are not re-attributable.

### 4.2 Regulatory alignment

- **EU AI Act Article 12 (logging requirements for high-risk AI systems).** Although agent runtimes are not yet uniformly classified high-risk under Article 6, the audit-trail HMAC feature in Cohort B is designed to meet Article 12 logging integrity expectations preemptively — tamper-evident logs, retention period customer-configurable, traceability of decisions back to shield versions.
- **GDPR Article 17 (right to erasure).** The § 4.1 deletion endpoint is the operationalization. We document in the engagement charter that requests are honored within 30 days; in practice, target 7 days.
- **GDPR Article 5(1)(c) (data minimization).** The § 3.2 "what we do not capture" list is the contract.
- **California CCPA / CPRA.** Same deletion endpoint covers consumer requests; no separate process.
- **SOC 2.** Not in scope for pilot; we will pursue Type 2 in parallel with GA prep but it is not a pilot blocker.

### 4.3 Customer data-handling document

A two-page PDF, written in plain English, ships with the pilot welcome email. It states:

- The § 3.1 list, verbatim.
- The § 3.2 list, verbatim.
- The 90-day retention.
- The deletion procedure (one command + how to verify it ran).
- Contact email for privacy questions (`privacy@vis.dev`, monitored daily).

If a prospect's legal team objects to anything in the document, we negotiate — we do not assume.

---

## 5. Tuning playbook

### 5.1 Thresholds per shield

Reference the synthetic baseline at `security/synthetic-fire-2026-05/regression-baseline.json` as the floor. A real-traffic threshold may not be looser than the synthetic baseline for the same shield + same attack class.

| Shield | Synthetic-baseline FP | Real-traffic FP target | Real-traffic FN target |
|--------|----------------------|------------------------|-----------------------|
| canary | 0.4% | ≤ 2% | ≤ 5% |
| package-gate | 1.1% | ≤ 4% | ≤ 8% |
| egress-monitor | 0.8% | ≤ 3% | ≤ 10% |
| capability-fence | n/a (advisory in pilot) | ≤ 6% (measured Cohort B) | ≤ 12% |
| audit-trail HMAC | 0% (deterministic) | 0% | n/a (integrity, not detection) |
| OTLP export | n/a | n/a | n/a (transport, not detection) |
| (reserved for week-12 review) | — | — | — |

FP rate = (customer-flagged FPs + auto-detected-FPs) / total shield events. FN rate = (customer-reported FNs + post-hoc-discovered FNs) / (total attacks in window, estimated via Cohort A baseline + 2x adjustment for unreported).

### 5.2 How to push tuning fixes

1. **Weekly tuning PR cadence.** Every Friday, the on-call shield engineer opens a PR titled `tune: <shield>-<week>-<delta>` updating threshold constants. PR description cites the Cohort telemetry rows that motivated the change.
2. **Regression-baseline.json gate.** Every tuning PR must run the synthetic harness and emit a fresh `regression-baseline.json`. If any synthetic attack class regresses by > 5% true-positive rate, the PR is held until the regression is investigated.
3. **Customer-side rollout.** Tuning fixes ship as a shield-version bump. Cohort A is auto-opted into the new version after 24h soak in a staging customer. Cohort B/C require explicit consent to auto-update; otherwise pinned.
4. **Rollback procedure.** Every shield version is reversible by config flag. A customer reporting a regression can pin to the previous version with one command; we expect at least one rollback per cohort.

### 5.3 Novel-attack-pattern intake

When a customer reports an FN (a real attack the shield missed):

1. Customer ships us the attack trace (with permission, anonymized).
2. We add a synthetic test case to `security/synthetic-fire-2026-05/` reproducing it.
3. We tune the relevant shield to catch it.
4. We confirm the new test case passes + no synthetic regression > 5%.
5. We ship the fix to the reporting customer first as a courtesy.
6. We backfill the fix to the rest of the cohort within 1 week.

---

## 6. Pilot exit criteria

The pilot graduates to GA when **all six** hold:

1. **FP rate < 5%** across all enabled-by-default shields, measured over a 4-week window, averaged across Cohort B + C customers.
2. **FN rate < 10%** for the same shield set, same window. FN is measured against the union of (customer-reported FNs) + (synthetic harness regression-baseline corpus).
3. **No critical novel attack surface uncovered in the last 2 weeks** of the pilot. "Critical" = a single missed attack class that would have a CVSS ≥ 7.0 if exploited.
4. **≥ 3 customers report "would pay for this"** in their week-12 check-in, on the record, with a price band attached (does not need to be the final GA price).
5. **OTLP export interoperability verified** with at least two third-party observability stacks (Datadog, Honeycomb, Grafana, Sentry — pick any two).
6. **Audit-trail HMAC verified end-to-end** — a customer's auditor (theirs, not ours) confirms the log integrity property is meaningful.

Any one failing → continue pilot, extend by 2 weeks, re-evaluate.

---

## 7. GA launch checklist

Operator deliverables before flipping the GA switch:

- [ ] **Operator runbooks updated** under `packages/safety/operator-wiring-2026-05/setup-runbooks/` for each shield, covering: deploy, configure, debug, rollback, escalate.
- [ ] **Pricing page drafted** and reviewed by 3 design partners. Three tiers (solo / team / enterprise); team tier price calibrated to the Cohort C feedback.
- [ ] **Support tier defined.** Tier 1 (community Discord, no SLA), Tier 2 (email, business-day SLA, included with team), Tier 3 (dedicated Slack channel, 4-hour SLA, enterprise add-on).
- [ ] **SLA published.** 99.5% uptime for telemetry endpoint (the shields are local; SLA covers our side of the wire). No SLA on detection accuracy — the synthetic + real-traffic numbers stand as honest disclosure.
- [ ] **Privacy policy + DPA template** published. DPA is signable as-is for EU customers without further negotiation in 80% of cases.
- [ ] **Public regression-baseline.json** mirrored to a stable URL so customers can verify our claims.
- [ ] **Status page** live, monitoring the telemetry endpoint + the shield-version distribution endpoint.
- [ ] **Launch post drafted** — names Cohort A customers who consented, links to the synthetic harness and gap analysis, no marketing hyperbole on detection rates.
- [ ] **30-day post-launch review scheduled** at week +4 to catch any cohort-of-one issues that the pilot missed.

---

## 8. What we communicate to design partners

### 8.1 Engagement charter (one page, signed at start of pilot)

- The cohort they're in and what shields are active.
- The telemetry contract (§ 3.1, § 3.2, verbatim).
- The privacy stance (§ 4.1, verbatim).
- The check-in cadence and what we'll ask in it.
- The incentive (§ 1.3).
- The exit clause (7 days notice, either side).

### 8.2 Technical onboarding (90 minutes, video call)

- Install the shield package.
- Walk through the config file together; identify what's advisory vs. blocking.
- Verify the local audit log is writing.
- Verify the telemetry opt-in toggle is in the customer's preferred state.
- Walk through the FP/FN report buttons in the IDE indicator.
- Give them the privacy email + the on-call engineer's contact for incidents.

### 8.3 Weekly check-in template (30 minutes)

1. **What did the shields catch this week?** Skim the audit log together; flag anything that surprised either side.
2. **Any FPs?** Triage on-call; agree on threshold adjustment if any.
3. **Any FNs?** Open the intake process (§ 5.3) if any.
4. **Any latency complaints from your engineers?** Cross-reference against the p99 telemetry.
5. **One open question for us.** They get a slot to push back on anything in the roadmap.
6. **Action items + owners + due date.** No meeting without a written followup within 24h.

### 8.4 Exit interview (end of cohort)

A 45-minute structured interview, recorded with consent. Questions:

- What would have caused you to drop the pilot? (Find the cliff edge.)
- What did you tell your team about us? (Detect framing drift.)
- Would you pay for this? At what price? On what tier? (Map willingness-to-pay.)
- What's the next shield you'd want us to build? (Inform post-GA roadmap.)
- Anything we promised and didn't deliver? (Trust audit.)

Transcripts feed the GA launch decision and the post-launch roadmap. They are not published.

---

## Closure

This package is the bridge from synthetic measurement to honest production claims. The synthetic harness proved we *can* detect known attacks; the pilot proves the detection holds against real traffic at acceptable FP cost. GA ships when the six exit criteria pass — not when the calendar says so, not when the launch post is ready, not when the investor pings. The honest-numbers contract that governs the synthetic harness governs the pilot too: an FP rate measurement is what it is, and the cohort timeline extends if the numbers say so.
