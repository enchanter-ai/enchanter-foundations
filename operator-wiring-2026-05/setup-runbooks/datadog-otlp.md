# Datadog OTLP Setup

Wire agent-foundations OTEL spans to Datadog APM via the OTLP HTTP exporter. Time: ~15 minutes.

## Prerequisites

- Datadog account with APM enabled.
- A Datadog API key with `apm_read`+`apm_write` scope.
- Site identifier: `datadoghq.com` (US1), `datadoghq.eu`, `us3.datadoghq.com`, `us5.datadoghq.com`, `ap1.datadoghq.com`, or `ddog-gov.com`.

## Step 1 — Get the API key

1. Datadog UI → Organization Settings → API Keys.
2. Click "+ New Key", label it `enchanter-agent-foundations`.
3. Copy the key once — Datadog only shows it on creation.

## Step 2 — Identify the OTLP intake endpoint

| Site | Endpoint |
|------|----------|
| US1  | `https://trace.agent.datadoghq.com` |
| EU   | `https://trace.agent.datadoghq.eu`  |
| US3  | `https://trace.agent.us3.datadoghq.com` |
| US5  | `https://trace.agent.us5.datadoghq.com` |
| AP1  | `https://trace.agent.ap1.datadoghq.com` |
| GOV  | `https://trace.agent.ddog-gov.com`  |

Datadog accepts OTLP/HTTP at `/api/v0.2/traces` (binary protobuf) on the trace agent intake. For non-agent direct intake, use the Datadog OpenTelemetry collector exporter — see below.

## Step 3 — Set env vars

Add to your operator shell profile or secret manager:

```bash
export DD_API_KEY="<paste-from-step-1>"
export DD_SITE="datadoghq.com"
export OTEL_EXPORTER_OTLP_ENDPOINT="https://trace.agent.datadoghq.com"
export OTEL_EXPORTER_OTLP_HEADERS="DD-API-KEY=${DD_API_KEY}"
export OTEL_SERVICE_NAME="enchanter-agent-foundations"
export OTEL_RESOURCE_ATTRIBUTES="deployment.environment=prod,service.version=1.0.0"
```

Recommended: store `DD_API_KEY` in your secret manager (Vault, AWS SSM, 1Password CLI). Do NOT commit it to git.

## Step 4 — Verify ingestion

From the kit root:

```bash
python3 verify/verify-otlp.py "$OTEL_EXPORTER_OTLP_ENDPOINT" "$DD_API_KEY"
```

Expected output:
```
[verify-otlp] target=https://trace.agent.datadoghq.com
[verify-otlp] sending synthetic span trace_id=...
[verify-otlp] HTTP 200 OK
[verify-otlp] PASS - span accepted by collector
[verify-otlp] Manual: confirm span visible in DD UI within 60s at:
              https://app.datadoghq.com/apm/traces?query=service:enchanter-agent-foundations
```

If the verify script returns non-200, see "Troubleshooting" below.

## Step 5 — Confirm visibility in UI

1. Open `https://app.<DD_SITE>/apm/traces`.
2. Filter `service:enchanter-agent-foundations`.
3. Within 60 seconds, the synthetic span (operation `verify.synthetic`) should appear.

If it's visible — the integration is live. Flip the operator config flag.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| HTTP 403 | Wrong API key scope | Re-create key with APM scopes |
| HTTP 401 | DD-API-KEY header missing or malformed | Check `OTEL_EXPORTER_OTLP_HEADERS` quoting |
| Span never visible | Wrong DD_SITE | Match site to your Datadog org region |
| DNS failure | Typo in endpoint | Use exact endpoint from Step 2 table |
| Timeout | Egress firewall blocks 443 to `trace.agent.*` | Allow-list the endpoint hostname |

## Rotation

API keys should rotate every 90 days. Update the secret store; restart the agent-foundations process.
