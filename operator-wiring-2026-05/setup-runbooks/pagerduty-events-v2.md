# PagerDuty Events API v2 Setup

Wire agent-foundations HIGH-severity advisories to a PagerDuty service via the Events API v2. Time: ~10 minutes.

## Prerequisites

- PagerDuty account with admin or manager role for the target service.
- A service object that owns the on-call rotation that should be paged.

## Step 1 — Create the integration

1. PagerDuty UI → Services → pick (or create) the service that receives agent-foundations pages.
2. Integrations tab → "+ Add an Integration".
3. Integration type: **Events API v2**.
4. Name: `enchanter-agent-foundations`.
5. After creation, PagerDuty shows an **Integration Key** (a 32-char hex string). Copy it.

This integration key — sometimes called the routing key — is what authenticates the event.

## Step 2 — Set env vars

```bash
export PD_INTEGRATION_KEY="<paste-from-step-1>"
export PD_EVENTS_URL="https://events.pagerduty.com/v2/enqueue"
```

`PD_EVENTS_URL` is fixed globally — same endpoint for US and EU customers (PagerDuty routes by integration key, not region).

## Step 3 — Verify

```bash
python3 verify/verify-pager.py "$PD_EVENTS_URL" "$PD_INTEGRATION_KEY"
```

Expected output:
```
[verify-pager] target=https://events.pagerduty.com/v2/enqueue
[verify-pager] sending synthetic HIGH event dedup_key=verify-synthetic-...
[verify-pager] HTTP 202 Accepted
[verify-pager] PASS - event accepted, dedup_key returned by PD
[verify-pager] Manual: confirm incident visible in PagerDuty:
               https://YOUR-ORG.pagerduty.com/incidents
[verify-pager] After confirming, RESOLVE the synthetic incident in the UI.
```

## Step 4 — Confirm + clean up

1. Open `https://<your-org>.pagerduty.com/incidents`.
2. The verify script creates a low-urgency synthetic incident titled `verify.synthetic — agent-foundations integration check`.
3. Confirm it appears.
4. **Resolve it manually** in the UI (or let the verify script auto-resolve — pass `--auto-resolve`).

Until resolved, the synthetic incident will follow the service's escalation policy. If your service auto-pages on-call, set the integration to "urgency: low" first, or use `--auto-resolve` on the verify script.

## Step 5 — Configure event routing (optional)

Recommended routing per agent-foundations severity:

| agent-foundations severity | PagerDuty severity | PagerDuty action |
|----------------------------|--------------------|-------------------|
| HIGH                       | `critical`         | trigger          |
| MEDIUM                     | `warning`          | trigger (low urgency) |
| LOW                        | (skip)             | route to Slack instead |
| RESOLVED                   | n/a                | `resolve` action with same `dedup_key` |

The `dedup_key` is the agent-foundations advisory ID — same incident_id deduplicates on PD's side.

## Payload shape (reference)

The verify script sends and the production emitter must send:

```json
{
  "routing_key": "<integration-key>",
  "event_action": "trigger",
  "dedup_key": "<advisory-id>",
  "payload": {
    "summary": "string ≤ 1024 chars",
    "source": "enchanter-agent-foundations",
    "severity": "critical | error | warning | info",
    "timestamp": "ISO-8601 UTC",
    "component": "string",
    "group": "string",
    "class": "string",
    "custom_details": { "...": "..." }
  }
}
```

Resolution uses the same `dedup_key` and `event_action: "resolve"`.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| HTTP 400 | Payload missing required field | Compare to shape above; `summary`, `source`, `severity` are required |
| HTTP 401 | Wrong / disabled integration key | Re-copy from Service → Integrations |
| HTTP 429 | Rate limit (120 req/min default) | Throttle emitter; batch advisories |
| Event accepted, no incident | Service's escalation policy blocks low-urgency | Check service config or use `severity: critical` |
| Incident never resolves | Resolve event used different `dedup_key` | dedup_key must match the triggering event exactly |

## Rotation

Integration keys rotate via Service → Integrations → click integration → "Reset". Old key invalidates immediately. Update secret store + restart emitter in one window.
