# External Gap — Real Customer Traffic

> What the synthetic-fire-2026-05 harness does NOT cover, and what we still
> need before production launch.

---

## What the synthetic harness covers

- **1300 events** across 5 benign session shapes + 1 adversarial bundle
  + 1 edge-case bundle.
- **8 plugins** measured with TP/FP/TN/FN, precision, recall, p99 runtime.
- **Reproducible** (fixed `random.seed`) — re-runs match exactly.
- **CI-wireable** — `run-report.py` exits non-zero on ≥5 percentage-point
  precision OR recall regression vs. the stored baseline.

This is enough to lock down **first-order** plugin behavior: known-shape
attacks, known-shape benign flows, known-shape edge cases. It's not
production fire.

---

## What the synthetic harness does NOT cover

### 1. Long-tail benign behavior

Real dev traffic has a distribution far wider than 5 fixed session
shapes. Examples NOT in the harness:

- **Polyglot repos** — Rust + WebAssembly + TS frontend in one repo
  produces tool-call sequences our session shapes don't model.
- **CI/CD-driven flows** — agent triggered by a webhook to triage a build
  failure: thousands of log lines fed into a single PostToolUse.
- **Region-specific URLs** — Asian / European / Russian-language docs
  sites, mirrors, BitBucket-style internal Atlassian hosts. The egress
  allowlist seeded here is US-Western-centric.
- **Niche tool ecosystems** — `kubectl`, `helm`, `terraform`, `ansible`,
  `bazel`, `buck2` — none exercised; each has its own destructive-command
  vocabulary action-guard does not yet recognize.
- **Internal package mirrors** — corp Artifactory/Nexus instances will
  trip egress-monitor's first-seen-domain logic; the synthetic doesn't
  exercise this.

### 2. Real attacker behavior

The 200 adversarial events are drawn from the canary fixture catalog
(20 OWASP-style injection patterns) plus our typosquat/CVE/exfil seeds.
Production attackers will:

- Combine techniques (injection + capability escalation + egress in one
  multi-turn flow) — the harness is per-event, not multi-turn.
- Stage attacks across sessions — `state/precedent-log.md` works at
  session boundary; cross-session attack tracking is not modeled.
- Probe with low-velocity, high-patience attacks — synthetic randomness
  doesn't reproduce a 4-week dwell-time.

### 3. Operational reality

- **Hook timing under load.** Synthetic runs measure plugin-logic ms in
  isolation. Real PostToolUse runs while the agent is also doing other
  work; lock contention on `state/*.jsonl` is not simulated.
- **State file growth.** Audit-trail at 1300 events shows ~30 MB/day
  projected; real volume varies by team size and could be 10×.
- **Hook failures.** Synthetic always succeeds. Production has filesystem
  full, permission errors, stale locks — the fail-open contract must be
  exercised.
- **Permission settings drift.** A developer who flips a setting in their
  user-level `settings.local.json` overrides project-level enforcement.
  Synthetic doesn't reproduce this.

---

## Recommended path to production

1. **≥ 4 weeks of opt-in production telemetry** before claiming
   production-grade FP/FN. The synthetic numbers calibrate the *shape* of
   the detectors; only real volume calibrates the *thresholds*.
2. **Two-tier rollout.** Phase A: advisory-only with `audit-trail` OTLP
   export to a central collector. Phase B: opt-in blocking for the two
   plugins that hit 100% precision in the synthetic harness (canary,
   capability-fence) and reach ≥ 99% precision on real traffic.
3. **Weekly review cadence.** A human reviews advisory hits weekly for
   the first month — synthetic numbers will under-predict noise from
   long-tail dev tools.
4. **Egress allowlist bootstrap.** Capture all unique fetched domains
   from the first 4 weeks; classify as benign/suspicious/unknown; commit
   the classified allowlist as `hydra/plugins/egress-shield/config/`.

---

## Mechanisms already in place to capture real-traffic metrics

- `hydra/plugins/audit-trail/state/log.jsonl` — every event is already
  recorded locally (HMAC-chained). The data exists; we just don't have
  4 weeks of it yet.
- `hydra/plugins/canary/state/hits.ndjson` — every canary fire is
  recorded. Empty today; would be populated on first real injection.
- `agent-foundations/compliance/soc2-evidence/evidence-collection-plan.md`
  — describes the cron-driven evidence-collection job that would
  aggregate per-plugin advisory counts weekly.

What's NOT yet in place:
- OTLP exporter (F-021 / F-024 in progress) — needed for centralized
  aggregation across multiple developers' machines.
- Per-developer opt-in telemetry toggle — needed for compliance.
- Schema versioning on advisory records — needed before claiming the data
  is comparable run-over-run after plugin code changes.

---

## Honest verdict

The synthetic harness reduces calibration risk substantially: we know
which plugins are noisy, which are quiet, which catch their attack class,
and which need pattern additions. It does NOT replace real production
fire. Treat the 2026-05 baseline as the floor; real traffic will reveal
new failure modes we have not yet seen and could not have invented.

**Real production fire remains the single biggest gap before launch.**
