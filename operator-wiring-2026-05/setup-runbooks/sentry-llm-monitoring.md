# Sentry LLM Monitoring Setup

Wire agent-foundations LLM traces + errors to Sentry's AI Monitoring product. Time: ~10 minutes.

## Prerequisites

- Sentry account on `sentry.io` (SaaS) or self-hosted `>= 24.1.0` (AI Monitoring requirement).
- Permission to create a project in the target organization.

## Step 1 — Create the project

1. Sentry UI → Projects → "+ Create Project".
2. Platform: pick **Python** (or your runtime). Project type: **AI / LLM** if available; otherwise pick **Python** and enable AI Monitoring under Project Settings → AI Monitoring.
3. Name: `enchanter-agent-foundations`.
4. After creation, Sentry shows the DSN. Copy it.

A DSN looks like:
```
https://abcdef0123456789@o123456.ingest.sentry.io/7890123
```

## Step 2 — Set env vars

```bash
export SENTRY_DSN="https://abcdef0123456789@o123456.ingest.sentry.io/7890123"
export SENTRY_ENVIRONMENT="prod"
export SENTRY_TRACES_SAMPLE_RATE="0.1"
export SENTRY_PROFILES_SAMPLE_RATE="0.0"
```

Sample rates:
- `traces_sample_rate=0.1` — 10% of traces are kept. Adjust per cost budget.
- `profiles_sample_rate=0.0` — profiling off; turn on only for diagnostic sessions.

## Step 3 — Verify

```bash
python3 verify/verify-sentry.py "$SENTRY_DSN"
```

Expected output:
```
[verify-sentry] dsn host=o123456.ingest.sentry.io project=7890123
[verify-sentry] sending synthetic LLM trace event_id=...
[verify-sentry] HTTP 200 OK
[verify-sentry] PASS - event accepted by Sentry
[verify-sentry] Manual: confirm event visible in Sentry UI within 30s:
                Issues tab, search "verify.synthetic"
```

## Step 4 — Confirm visibility

1. Sentry UI → your new project → Issues.
2. Filter for `verify.synthetic` or the event ID from the verify script output.
3. The event should appear within 30 seconds.

For AI Monitoring view: Insights → AI → LLM Monitoring → filter on service `enchanter-agent-foundations`.

## Step 5 — Configure issue routing (optional but recommended)

Recommended alert rules:
- Severity `error` or `fatal` → page via PagerDuty (configure under Alerts → New Alert Rule).
- LLM cost spike (10× rolling baseline) → Slack channel.
- Latency p99 > 30s → Slack channel.

These rules live in Sentry, not in this kit — set them once per project.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| HTTP 401 | Invalid DSN (truncated, wrong project) | Re-copy DSN from Project Settings → Client Keys |
| HTTP 429 | Rate limit hit | Lower `traces_sample_rate` or upgrade plan |
| Event sent, not visible | Inbound filter dropping it | Check Project Settings → Inbound Filters |
| DNS failure on `.ingest.sentry.io` | Egress firewall | Allow-list `*.ingest.sentry.io` and `*.sentry.io` |
| DSN host mismatch self-hosted | Self-hosted instance | Replace host portion of DSN; keep public-key + project-id |

## DSN hygiene

- The DSN is a **public** key — it's safe in client builds but should NOT be exposed in public repos because it lets anyone send events to your project.
- Store in secret manager for server-side use.
- Rotate via Project Settings → Client Keys → "Disable" + create new.

## Cost guard

Sentry charges per event. The verify script sends exactly one event. Production sampling at 10% is the recommended starting point; tune after first week of traffic.
