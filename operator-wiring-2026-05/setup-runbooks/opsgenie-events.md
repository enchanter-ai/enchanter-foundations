# Opsgenie Events Setup

Wire agent-foundations advisories to an Opsgenie team via the Alerts API v2. Time: ~10 minutes.

## Prerequisites

- Opsgenie account (Atlassian Cloud or standalone).
- A team that owns the on-call rotation.
- API integration permission for that team.

## Step 1 — Create the API integration

1. Opsgenie UI → Teams → pick the target team.
2. Integrations tab → "Add Integration" → **API**.
3. Name: `enchanter-agent-foundations`.
4. Enable: ON. Read access: ON. Suppress notifications: OFF (unless testing).
5. Copy the **API Key** (UUID format).

## Step 2 — Identify region endpoint

| Region | Endpoint |
|--------|----------|
| US     | `https://api.opsgenie.com/v2/alerts` |
| EU     | `https://api.eu.opsgenie.com/v2/alerts` |

Check your Opsgenie URL: `app.opsgenie.com` (US) vs `app.eu.opsgenie.com` (EU).

## Step 3 — Set env vars

```bash
export OPSGENIE_API_KEY="<uuid-from-step-1>"
export OPSGENIE_URL="https://api.opsgenie.com/v2/alerts"
export OPSGENIE_TEAM="agent-foundations-oncall"
```

## Step 4 — Verify

```bash
python3 verify/verify-pager.py "$OPSGENIE_URL" "$OPSGENIE_API_KEY" --provider opsgenie
```

Expected output:
```
[verify-pager] target=https://api.opsgenie.com/v2/alerts (opsgenie)
[verify-pager] sending synthetic alert alias=verify-synthetic-...
[verify-pager] HTTP 202 Accepted
[verify-pager] requestId=...
[verify-pager] PASS - alert accepted by Opsgenie
[verify-pager] Manual: confirm alert visible in Opsgenie UI:
               https://app.opsgenie.com/alert/list
[verify-pager] After confirming, close the synthetic alert in the UI.
```

## Step 5 — Confirm + clean up

1. Opsgenie UI → Alerts.
2. The synthetic alert is titled `verify.synthetic — agent-foundations integration check`, priority `P5`.
3. Close it manually (or use `--auto-resolve` on the verify script).

## Payload shape (reference)

The production emitter sends:

```json
{
  "message": "string ≤ 130 chars",
  "alias": "<advisory-id>",
  "description": "string ≤ 15000 chars",
  "responders": [{"name": "agent-foundations-oncall", "type": "team"}],
  "priority": "P1 | P2 | P3 | P4 | P5",
  "source": "enchanter-agent-foundations",
  "tags": ["agent-foundations", "<advisory-category>"],
  "details": { "...": "..." }
}
```

The `alias` field deduplicates — same alias re-uses the same alert until closed.

| agent-foundations severity | Opsgenie priority |
|----------------------------|-------------------|
| HIGH                       | P1                |
| MEDIUM                     | P3                |
| LOW                        | P5 (or skip)      |

Closing an alert: `POST /v2/alerts/<alias>/close?identifierType=alias` with `Authorization: GenieKey <API_KEY>`.

## Authorization header

All requests use:
```
Authorization: GenieKey <OPSGENIE_API_KEY>
```

Note the literal word `GenieKey` (not `Bearer`).

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| HTTP 401 | Missing `GenieKey` prefix | Header must be `Authorization: GenieKey <key>` |
| HTTP 403 | API key disabled or wrong team | Check integration enabled + team has alert access |
| HTTP 422 | Payload validation | `message` field missing or > 130 chars |
| HTTP 429 | Rate limit | Default 130 req/min; throttle batch |
| Wrong region | EU key against US endpoint | Match endpoint to your tenant region |

## Rotation

Rotate via Team → Integrations → edit → "Regenerate Key". Old key invalidates immediately.
