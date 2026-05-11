# Operator Wiring Kit — agent-foundations (2026-05)

Scaffolding for an operator to wire agent-foundations into their observability + paging stack in under a day. Config + verify, not code.

## What's in the box

```
operator-wiring-2026-05/
├── README.md                 ← this file
├── setup-checklist.md        ← 50-step master checklist; the "one runbook to rule them all"
├── config-validator.py       ← stdlib config-file linter (paging-config.json, otel-config.yaml)
├── setup-runbooks/           ← one runbook per integration; copy-paste env vars + verify command
│   ├── datadog-otlp.md
│   ├── sentry-llm-monitoring.md
│   ├── pagerduty-events-v2.md
│   ├── opsgenie-events.md
│   ├── slack-webhook.md
│   └── splunk-otlp.md
├── verify/                   ← stdlib-only probes; send a synthetic event, confirm 2xx
│   ├── verify-otlp.py        (Datadog, Splunk, any OTLP/HTTP collector)
│   ├── verify-pager.py       (PagerDuty + Opsgenie via --provider flag)
│   ├── verify-sentry.py      (Sentry envelope API)
│   ├── verify-slack.py       (Slack incoming webhooks)
│   └── verify-all.sh         (master orchestrator; reads env, runs all)
└── mock-endpoints/           ← stdlib HTTP servers; smoke-test verifies without real creds
    ├── mock-otlp-collector.py    (port 4318)
    ├── mock-pagerduty.py         (port 8123)
    ├── mock-slack.py             (port 8124)
    ├── mock-opsgenie.py          (port 8125)
    └── run-mocks.sh              (start | stop | status)
```

## What this kit IS

- **Setup runbooks** the operator follows once per integration, with copy-paste env vars and a one-command verify at the end.
- **Mock endpoints** the operator (or this kit's CI) can run locally to confirm the kit itself works before pointing at real services.
- **Config validators** that lint the operator's `paging-config.json` and `otel-config.yaml` for obvious mistakes (placeholder keys, malformed URLs, unreachable hostnames).
- **Verify scripts** that take the operator's real credentials and send one synthetic event per integration, returning a clear `PASS`/`FAIL` with a manual UI confirmation step at the end.

## What this kit is NOT

- **Not a credential broker.** We don't store or proxy the operator's API keys. Every verify script takes the key as an argument or env var, sends it directly to the vendor's endpoint, and exits.
- **Not a runtime integration.** Once the operator has confirmed each integration with the verify scripts, they wire the same endpoints + secret-manager references into agent-foundations' own config. This kit's job ends at "verify PASSED — now flip the config flag."
- **Not autonomous.** Every verify ends with a manual UI confirmation step. The kit can confirm the HTTP layer is wired; only a human can confirm the event hit the right dashboard / paged the right team / pinged the right Slack channel.

## How to use (TL;DR)

1. Read `setup-checklist.md` end-to-end before starting. Estimate ~1 day for a full rollout, ~15 minutes per integration.
2. Smoke-test the kit against the mocks (Phase 1 of the checklist).
3. For each integration in scope, open its runbook, follow it through to its verify step.
4. Run `verify/verify-all.sh` once at the end as a regression check.
5. Capture screenshots of the synthetic events in each backend's UI for the audit trail.

## Pre-shipped vs operator-provided

| Pre-shipped (this kit) | Operator-provided |
|------------------------|-------------------|
| All runbooks, verify scripts, mocks, config validator | Real DD_API_KEY, SENTRY_DSN, PD_INTEGRATION_KEY, SLACK_WEBHOOK_URL, etc. |
| Endpoint URL tables per region | Choice of region, environment name, on-call team |
| Payload shape references | The actual `paging-config.json` / `otel-config.yaml` files |
| Failure-mode troubleshooting tables | The judgement of whether the synthetic event reached the right channel |

## Bridge to the audit-trail plugins

Once verifies are green, agent-foundations' own emitters (defined in the audit-trail plugins) point at the same endpoints the verify scripts just exercised. Concretely:

- The OTLP exporter inside agent-foundations uses `OTEL_EXPORTER_OTLP_ENDPOINT` and `OTEL_EXPORTER_OTLP_HEADERS` — the same env vars the runbook + verify-otlp use. Confirming `verify-otlp.py` works means agent-foundations' tracing will work the moment it starts up with the same env.
- The pager + Slack emitters consume `paging-config.json`. The same JSON file is what `config-validator.py` lints. If the validator passes and `verify-pager.py` / `verify-slack.py` pass against the keys referenced in the file, the emitters will succeed too.
- Sentry init reads `SENTRY_DSN` from env. If `verify-sentry.py` passes, the runtime client will accept the same DSN.

The contract between this kit and the audit-trail plugins is: **same env vars, same payload shapes, same endpoints**. No additional wiring needed.

## Constraints honored

- Python stdlib only — no pip install, no virtual env required.
- All verifies fail-fast with clear messages on missing creds (no false PASS).
- Mocks listen only on `127.0.0.1` by default; nothing exposed externally.
- No commit / push from inside this kit; it's a static toolkit.

## Operating the kit

```
# smoke-test the kit (no real creds needed)
mock-endpoints/run-mocks.sh start
verify/verify-otlp.py http://localhost:4318 --no-auth
verify/verify-pager.py http://localhost:8123/v2/enqueue mock-key
verify/verify-slack.py http://localhost:8124/services/Tmock/Bmock/mocksecret
mock-endpoints/run-mocks.sh stop

# real wiring (operator provides creds via env)
export DD_API_KEY=... SENTRY_DSN=... PD_INTEGRATION_KEY=... SLACK_WEBHOOK_URL=...
verify/verify-all.sh

# lint operator config
config-validator.py path/to/paging-config.json --all
```

## Failure modes the kit catches

| Symptom | Caught by | How |
|---------|-----------|-----|
| Wrong API key | verify script | HTTP 401/403, clear hint about header name |
| Wrong region endpoint | verify script | DNS failure or HTTP 404 |
| Placeholder key in config | config-validator | `pager.integration_key is empty or a placeholder` |
| Malformed webhook URL | config-validator | URL parser + DNS resolution check |
| Block Kit shape wrong | mock-slack | 400 with `invalid_blocks` |
| Missing required PagerDuty payload field | mock-pagerduty | 400 with field list |
| Egress firewall blocks vendor | verify script | network error with hostname |

## Failure modes the kit does NOT catch

- Integration key has wrong scope (returns 200 but events vanish into a black hole) → manual UI confirmation step exists for this.
- Wrong on-call team assigned → operator must check the page actually wakes the right person.
- Sentry event filtered by an inbound rule → manual confirmation step covers this.

These are why every runbook ends with "Manual: confirm visible in UI."

## Support

If a verify script returns an error not documented in the runbook troubleshooting table, file an issue with:
- The exact command + output
- The integration vendor + region
- The HTTP status and any response-body excerpt

Do NOT include the API key in the issue.
