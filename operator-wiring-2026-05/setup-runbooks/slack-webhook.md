# Slack Incoming Webhook Setup

Wire agent-foundations advisories (MEDIUM/LOW severity) to a Slack channel via Incoming Webhooks. Time: ~5 minutes.

## Prerequisites

- Slack workspace where you can install apps.
- Permission to create a Slack app (or use an existing one with `incoming-webhook` scope).

## Step 1 — Create the Slack app + webhook

1. https://api.slack.com/apps → "Create New App" → "From scratch".
2. App name: `enchanter-agent-foundations`. Workspace: your target workspace.
3. Features → **Incoming Webhooks** → toggle ON.
4. Click "Add New Webhook to Workspace".
5. Pick the target channel (e.g., `#agent-foundations-alerts`).
6. Authorize. Slack returns a webhook URL like:

```
https://hooks.slack.com/services/T0123456/B0123456/abcdefABCDEFabcdefABCDEF
```

The URL is the **only** auth — anyone with it can post. Treat as a secret.

## Step 2 — Set env vars

```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/T0123456/B0123456/abcdefABCDEFabcdefABCDEF"
export SLACK_DEFAULT_CHANNEL="#agent-foundations-alerts"
```

(Channel is encoded in the webhook itself; `SLACK_DEFAULT_CHANNEL` is documentation, not enforcement.)

## Step 3 — Verify

```bash
python3 verify/verify-slack.py "$SLACK_WEBHOOK_URL"
```

Expected output:
```
[verify-slack] target=https://hooks.slack.com/services/T01.../B01.../****
[verify-slack] sending synthetic advisory
[verify-slack] HTTP 200 OK
[verify-slack] response body: ok
[verify-slack] PASS - posted to channel
[verify-slack] Manual: confirm message visible in #agent-foundations-alerts
```

## Step 4 — Confirm visibility

Open Slack → the channel you wired → look for a message authored by the webhook app titled:

> `[verify.synthetic] agent-foundations operator-wiring integration check`

The post includes a structured block with severity, summary, and a "RESOLVE" placeholder link.

## Payload shape (production)

The emitter sends `application/json`:

```json
{
  "text": "fallback plain text for notifications",
  "blocks": [
    {
      "type": "header",
      "text": { "type": "plain_text", "text": "[MEDIUM] advisory summary" }
    },
    {
      "type": "section",
      "fields": [
        { "type": "mrkdwn", "text": "*Severity*\nMEDIUM" },
        { "type": "mrkdwn", "text": "*Category*\nrate-limit" },
        { "type": "mrkdwn", "text": "*Source*\nenchanter-agent-foundations" },
        { "type": "mrkdwn", "text": "*Trace*\n<https://dd-url|view>" }
      ]
    },
    {
      "type": "context",
      "elements": [{ "type": "mrkdwn", "text": "advisory_id: `<uuid>`" }]
    }
  ]
}
```

Slack accepts up to 50 blocks per message; agent-foundations advisories use 3-4.

## Routing strategy

| agent-foundations severity | Channel | Reason |
|----------------------------|---------|--------|
| HIGH | `#agent-foundations-pager` (mirror) | Backup of PagerDuty/Opsgenie for awareness |
| MEDIUM | `#agent-foundations-alerts` | Primary review channel |
| LOW | `#agent-foundations-noise` | Skim, batch-review |

Use a separate webhook per channel. Webhooks are 1:1 with channels.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| HTTP 404 / `invalid_token` | Webhook revoked or wrong URL | Re-check URL; revoke + recreate if compromised |
| HTTP 403 | App removed from workspace | Reinstall app under app management |
| HTTP 400 / `invalid_blocks` | Block structure malformed | Validate against Block Kit Builder |
| HTTP 429 / `rate_limited` | Slack: 1 req/sec/webhook | Throttle emitter; batch LOW advisories per minute |
| Message sent, channel empty | Wrong channel in webhook URL | Reauthorize webhook to correct channel |

## Rotation

Webhook URLs don't expire but can be revoked: api.slack.com/apps → your app → Incoming Webhooks → trash icon. Create a new one and update secret store.

## Security note

A leaked webhook URL = anyone can post to that channel. Audit posts monthly; if you see unexpected messages, revoke + recreate.
