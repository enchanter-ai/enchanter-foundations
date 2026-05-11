#!/usr/bin/env bash
# verify-all.sh — run every verify-* probe and emit a green/red checklist.
#
# Reads creds from env vars (preferred) or skips with "MISSING".
#
# Env vars consumed:
#   OTEL_EXPORTER_OTLP_ENDPOINT, DD_API_KEY  (Datadog OTLP)
#   SPLUNK_OTLP_ENDPOINT, SPLUNK_ACCESS_TOKEN   (optional, Splunk OTLP)
#   SENTRY_DSN                                  (Sentry)
#   PD_EVENTS_URL, PD_INTEGRATION_KEY           (PagerDuty)
#   OPSGENIE_URL, OPSGENIE_API_KEY              (Opsgenie)
#   SLACK_WEBHOOK_URL                           (Slack)
#
# Exit codes:
#   0 = every attempted verify passed
#   1 = at least one failed
#   2 = nothing to verify (all integrations missing creds)

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="${PYTHON:-python3}"

RESULTS=()
ANY_RUN=0
ANY_FAIL=0

run_check() {
  # $1 = label, $2 = command (string), $3 = "skip-reason" if creds missing else ""
  local label="$1"
  local cmd="$2"
  local skip_reason="${3:-}"
  if [[ -n "$skip_reason" ]]; then
    RESULTS+=("[ -- ] $label — SKIP ($skip_reason)")
    return
  fi
  ANY_RUN=1
  echo "----- $label -----"
  if eval "$cmd"; then
    RESULTS+=("[ OK ] $label")
  else
    ANY_FAIL=1
    RESULTS+=("[FAIL] $label")
  fi
  echo
}

# ---- Datadog OTLP ----
if [[ -n "${DD_API_KEY:-}" && -n "${OTEL_EXPORTER_OTLP_ENDPOINT:-}" ]]; then
  run_check "datadog-otlp" \
    "\"$PY\" \"$SCRIPT_DIR/verify-otlp.py\" \"$OTEL_EXPORTER_OTLP_ENDPOINT\" \"$DD_API_KEY\"" \
    ""
else
  run_check "datadog-otlp" "" "missing DD_API_KEY or OTEL_EXPORTER_OTLP_ENDPOINT"
fi

# ---- Splunk OTLP ----
if [[ -n "${SPLUNK_ACCESS_TOKEN:-}" && -n "${SPLUNK_OTLP_ENDPOINT:-}" ]]; then
  run_check "splunk-otlp" \
    "\"$PY\" \"$SCRIPT_DIR/verify-otlp.py\" \"$SPLUNK_OTLP_ENDPOINT\" \"$SPLUNK_ACCESS_TOKEN\" --header-name X-SF-Token" \
    ""
else
  run_check "splunk-otlp" "" "missing SPLUNK_ACCESS_TOKEN or SPLUNK_OTLP_ENDPOINT"
fi

# ---- Sentry ----
if [[ -n "${SENTRY_DSN:-}" ]]; then
  run_check "sentry" \
    "\"$PY\" \"$SCRIPT_DIR/verify-sentry.py\" \"$SENTRY_DSN\"" \
    ""
else
  run_check "sentry" "" "missing SENTRY_DSN"
fi

# ---- PagerDuty ----
if [[ -n "${PD_INTEGRATION_KEY:-}" ]]; then
  PD_URL="${PD_EVENTS_URL:-https://events.pagerduty.com/v2/enqueue}"
  run_check "pagerduty" \
    "\"$PY\" \"$SCRIPT_DIR/verify-pager.py\" \"$PD_URL\" \"$PD_INTEGRATION_KEY\" --provider pagerduty" \
    ""
else
  run_check "pagerduty" "" "missing PD_INTEGRATION_KEY"
fi

# ---- Opsgenie ----
if [[ -n "${OPSGENIE_API_KEY:-}" ]]; then
  OG_URL="${OPSGENIE_URL:-https://api.opsgenie.com/v2/alerts}"
  run_check "opsgenie" \
    "\"$PY\" \"$SCRIPT_DIR/verify-pager.py\" \"$OG_URL\" \"$OPSGENIE_API_KEY\" --provider opsgenie" \
    ""
else
  run_check "opsgenie" "" "missing OPSGENIE_API_KEY"
fi

# ---- Slack ----
if [[ -n "${SLACK_WEBHOOK_URL:-}" ]]; then
  run_check "slack" \
    "\"$PY\" \"$SCRIPT_DIR/verify-slack.py\" \"$SLACK_WEBHOOK_URL\"" \
    ""
else
  run_check "slack" "" "missing SLACK_WEBHOOK_URL"
fi

echo "================ summary ================"
for r in "${RESULTS[@]}"; do
  echo "$r"
done
echo "========================================="

if [[ "$ANY_RUN" -eq 0 ]]; then
  echo "verify-all: no integrations had creds set; nothing to verify." >&2
  exit 2
fi
if [[ "$ANY_FAIL" -ne 0 ]]; then
  echo "verify-all: at least one integration failed." >&2
  exit 1
fi
echo "verify-all: all attempted integrations PASSED. Manual UI confirmation still required per integration."
exit 0
