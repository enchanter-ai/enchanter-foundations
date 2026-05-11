# Splunk Observability Cloud OTLP Setup

Wire agent-foundations OTEL spans + logs to Splunk Observability Cloud (formerly SignalFx) via OTLP. Time: ~15 minutes.

## Prerequisites

- Splunk Observability Cloud account.
- Admin permission to create an access token.
- Realm identifier (visible in URL: `app.<REALM>.signalfx.com`, e.g., `us0`, `us1`, `eu0`).

## Step 1 — Create the access token

1. Splunk Observability UI → Settings → Access Tokens.
2. "+ New Token".
3. Name: `enchanter-agent-foundations`.
4. Authorization scope: include **INGEST** (required for spans, metrics, logs).
5. Copy the token string.

## Step 2 — Identify realm + endpoint

| Realm | OTLP HTTP endpoint |
|-------|--------------------|
| us0   | `https://ingest.us0.signalfx.com/v2/trace/otlp` |
| us1   | `https://ingest.us1.signalfx.com/v2/trace/otlp` |
| eu0   | `https://ingest.eu0.signalfx.com/v2/trace/otlp` |
| ap0   | `https://ingest.ap0.signalfx.com/v2/trace/otlp` |

For OTLP/HTTP via the OpenTelemetry Collector (recommended for production), the collector exports to the realm endpoint internally. For direct intake (no collector), use the URLs above.

## Step 3 — Set env vars

```bash
export SPLUNK_ACCESS_TOKEN="<paste-from-step-1>"
export SPLUNK_REALM="us0"
export OTEL_EXPORTER_OTLP_ENDPOINT="https://ingest.${SPLUNK_REALM}.signalfx.com/v2/trace/otlp"
export OTEL_EXPORTER_OTLP_HEADERS="X-SF-Token=${SPLUNK_ACCESS_TOKEN}"
export OTEL_SERVICE_NAME="enchanter-agent-foundations"
export OTEL_RESOURCE_ATTRIBUTES="deployment.environment=prod,service.version=1.0.0"
```

## Step 4 — (Optional) Configure OpenTelemetry Collector

For production, run the Splunk-distributed OpenTelemetry collector and point agent-foundations at it locally. Collector config snippet (`otel-collector.yaml`):

```yaml
receivers:
  otlp:
    protocols:
      http: { endpoint: 0.0.0.0:4318 }
      grpc: { endpoint: 0.0.0.0:4317 }
exporters:
  sapm:
    access_token: ${SPLUNK_ACCESS_TOKEN}
    endpoint: https://ingest.${SPLUNK_REALM}.signalfx.com/v2/trace
service:
  pipelines:
    traces:
      receivers: [otlp]
      exporters: [sapm]
```

Then point agent-foundations at the local collector:
```bash
export OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4318"
unset OTEL_EXPORTER_OTLP_HEADERS  # collector adds the token
```

## Step 5 — Verify

Direct intake:
```bash
python3 verify/verify-otlp.py "$OTEL_EXPORTER_OTLP_ENDPOINT" "$SPLUNK_ACCESS_TOKEN" --header-name X-SF-Token
```

Via local collector:
```bash
python3 verify/verify-otlp.py "http://localhost:4318" --no-auth
```

Expected output:
```
[verify-otlp] target=https://ingest.us0.signalfx.com/v2/trace/otlp
[verify-otlp] sending synthetic span trace_id=...
[verify-otlp] HTTP 200 OK
[verify-otlp] PASS - span accepted by collector
[verify-otlp] Manual: confirm trace visible in Splunk APM within 60s at:
              https://app.us0.signalfx.com/#/apm
```

## Step 6 — Confirm visibility

1. Splunk Observability UI → APM → Traces.
2. Filter `service.name: enchanter-agent-foundations`.
3. The synthetic span (operation `verify.synthetic`) should appear within 60s.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| HTTP 401 | Wrong / missing `X-SF-Token` | Header must be exact, case-sensitive |
| HTTP 403 | Token lacks INGEST scope | Recreate with INGEST scope |
| HTTP 404 | Wrong realm in URL | Match URL realm to your tenant |
| Trace ingested but not visible | Service name typo (case-sensitive) | Match service name across env + UI filter |
| DNS failure | Egress firewall | Allow-list `*.signalfx.com` |

## Token hygiene

- Tokens don't auto-rotate — set a 90-day reminder.
- Disable old tokens (Settings → Access Tokens → toggle off) before deleting; gives a 24h grace.
- Never commit tokens. Even default `INGEST`-only scope is enough to spam your account.
