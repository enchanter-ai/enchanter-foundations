# Operator Wiring Kickoff — Day-1 Walkthrough

Audience: the on-call operator bringing each integration live for the first time. This is a checklist, not an engineering spec. If a step asks you to decide architecture, stop and escalate — the runbook owns the decisions, you own the execution.

Integrations in scope: Datadog, Sentry, PagerDuty, Opsgenie, Slack, Splunk.

All shipped artifacts live under `packages/safety/operator-wiring-2026-05/`:

- `setup-runbooks/<integration>.md` — one runbook per integration (cred fields, env vars, post-setup smoke test)
- `verify/verify-all.sh` — single-entry verifier, returns non-zero on any failure
- `verify/<integration>.sh` — per-integration probe (called by verify-all.sh)
- `mock-endpoints/` — local stand-ins (docker-compose) you hit before real SaaS creds

Estimated total Day-1 wall time: 4–6 hours if no SaaS access blockers, 1–2 days if creds need procurement.

---

## 1. Day-1 master checklist

Run these in order. Do not skip ahead — step N's verify is step N+1's precondition.

### Cold start (steps 1–6)

1. Clone the repo at the tag named in `MACRO_ROADMAP.md` § Operator-wiring. Verify `packages/safety/operator-wiring-2026-05/` is present.
2. Copy `operator-wiring-2026-05/.env.example` to `.env.local`. Do NOT commit this file.
3. Install prereqs: Docker Desktop running, `jq`, `curl`, `bash` (Git Bash on Windows is fine).
4. From `operator-wiring-2026-05/mock-endpoints/`, run `docker compose up -d`. Confirm all six mock services reach healthy status (`docker compose ps`).
5. Export the mock-mode flag: `export OPERATOR_WIRING_MODE=mock`.
6. Run `./verify/verify-all.sh`. Expect all six integrations PASS against the mocks. If any FAIL here, fix Docker/network before touching real creds.

### Credential acquisition (steps 7–12)

See § 2 below for per-integration cred steps. Work them in this order — easiest first builds momentum:

7. Slack — webhook URL (10 min)
8. Sentry — DSN (15 min)
9. PagerDuty — service integration key (20 min)
10. Opsgenie — API key + team (20 min)
11. Datadog — API + APP key, confirm DD_SITE (30 min)
12. Splunk — HEC token + endpoint (45 min, often gated by InfoSec)

Paste each into `.env.local` under the variable named at the top of the matching `setup-runbooks/<integration>.md`.

### Single-integration verify (steps 13–18)

After each cred lands, switch that integration to real mode and verify:

13. `export OPERATOR_WIRING_MODE=real_slack` → `./verify/slack.sh` → expect a real test message in the configured channel.
14. `export OPERATOR_WIRING_MODE=real_sentry` → `./verify/sentry.sh` → expect a synthetic error event in the Sentry project's issue list within 60s.
15. `export OPERATOR_WIRING_MODE=real_pagerduty` → `./verify/pagerduty.sh` → expect a test incident in the service, then auto-resolve.
16. `export OPERATOR_WIRING_MODE=real_opsgenie` → `./verify/opsgenie.sh` → expect a test alert on the configured team, then close.
17. `export OPERATOR_WIRING_MODE=real_datadog` → `./verify/datadog.sh` → expect a test metric (`operator_wiring.verify=1`) and a test event in Events Explorer.
18. `export OPERATOR_WIRING_MODE=real_splunk` → `./verify/splunk.sh` → expect a test event in the configured HEC index.

### All-green and handoff (steps 19–24)

19. `export OPERATOR_WIRING_MODE=real_all` → `./verify/verify-all.sh` → all six PASS.
20. Capture the verify-all.sh output to `operator-wiring-2026-05/state/verify-day1-<YYYYMMDD>.log`. Commit the log (not `.env.local`).
21. Confirm each integration's notification reached its target human (Slack message visible, PagerDuty incident acknowledged, etc.). Operator-visible ≠ delivered.
22. File the Day-1 completion record per `MACRO_ROADMAP.md` instructions (the brief notice, not a full status report).
23. Stop the mock-endpoints stack: from `mock-endpoints/`, `docker compose down`. The mocks are dev aids, not load-bearing in real mode.
24. Hand off `.env.local` location and the verify log to the dev team lead.

### Resilience checks (steps 25–30)

25. Disable network for 30s, run `./verify/datadog.sh`. Expect a clean retry-then-fail (not a hang). Document timeout actually observed.
26. Re-enable network. Re-run; expect PASS.
27. Rotate the Slack webhook URL by adding a second one in Slack, swap into `.env.local`, re-run `verify/slack.sh`. Confirms rotation works without redeploy.
28. Force-trigger one alert path end-to-end (Sentry error → PagerDuty incident → Slack message). Confirms the chain, not just each link.
29. Open `verify/verify-all.sh` and read it once — you will run it as a cron later (§ 7).
30. Note any deviation from this checklist in `state/operator-deviations.md` for the next operator's benefit.

---

## 2. Credential acquisition matrix

| Integration | Where to get it | Env var(s) | Time | Gotcha |
|-------------|-----------------|------------|------|--------|
| Datadog | Org Settings → API Keys (create new) and Application Keys (create new). DD_SITE depends on your tenant: `datadoghq.com` (US1), `datadoghq.eu` (EU1), `us3.datadoghq.com`, `us5.datadoghq.com`, `ap1.datadoghq.com`. | `DD_API_KEY`, `DD_APP_KEY`, `DD_SITE` | 30 min | Wrong DD_SITE returns silent 403; always check the URL of your dashboard. |
| Sentry | Project → Settings → Client Keys (DSN). Pick the right project; new project takes 2 min. | `SENTRY_DSN` | 15 min | EU tenants have `*.ingest.de.sentry.io`. Using a US DSN against an EU org fails with 401. |
| PagerDuty | Service → Integrations → Add integration → Events API v2. Copy the **Integration Key** (32-char hex), NOT the API token. | `PAGERDUTY_ROUTING_KEY` | 20 min | Use Events API v2 (`/v2/enqueue`), not the legacy Generic Events API. |
| Opsgenie | Teams → <your team> → Integrations → API → API Key. Note region: `api.opsgenie.com` (US) vs `api.eu.opsgenie.com` (EU). | `OPSGENIE_API_KEY`, `OPSGENIE_REGION` | 20 min | Account-level keys exist but the runbook uses team-scoped keys. |
| Slack | App Directory → Incoming Webhooks → Add to channel. Copy the webhook URL. | `SLACK_WEBHOOK_URL` | 10 min | Webhooks scoped to a single channel; one URL per channel you write to. |
| Splunk | Settings → Data Inputs → HTTP Event Collector → New Token. Copy token + note the HEC URL (often `https://<host>:8088/services/collector`). | `SPLUNK_HEC_TOKEN`, `SPLUNK_HEC_URL` | 45 min | InfoSec often gates HEC; allow a buffer for ticket time. Self-signed certs may force `SPLUNK_HEC_INSECURE=1` in dev only. |

Anything procurement-blocked: log it in `state/cred-blockers.md` with the ticket number. Do not stall Day-1 on one integration — finish the others and circle back.

---

## 3. Verification sequence

Always: mock first, real second. Two reasons:

- Mock failures isolate to the local environment (Docker, network, scripts). Real-cred failures conflate environment, creds, and SaaS-side state.
- Mock endpoints accept any token. If the mock fails, fixing real creds will not unblock you.

### Mock pass criteria

`./verify/verify-all.sh` in `OPERATOR_WIRING_MODE=mock`:

- All six integrations: `PASS` in the summary table.
- Exit code 0.
- Each per-integration script prints exactly one line per probe (request sent, response received).

### Real pass criteria

Per-integration `./verify/<integration>.sh` in its `real_<name>` mode:

- HTTP 2xx from the SaaS endpoint.
- Human-observable side effect (message in channel, incident in service, event in index).
- Cleanup step succeeded (test incident auto-resolved, test alert closed, test event tagged `verify=true`).

If 2xx returns but the human-observable side effect doesn't appear: that's a routing issue (wrong channel, wrong service), not a creds issue. Re-check the runbook's "post-setup wiring" section.

---

## 4. Common failure modes

| Symptom | Diagnosis | Fix |
|---------|-----------|-----|
| `curl: (6) Could not resolve host` for any SaaS endpoint | Corporate DNS blocks the SaaS domain | Request InfoSec allowlist; in the interim, use the mock-endpoints stack and document the block. |
| Datadog probe returns 403 with no body | Wrong DD_SITE for your tenant | Open your DD dashboard, read the URL, set DD_SITE to match. US1 uses bare `datadoghq.com`; everything else uses a region prefix. |
| Sentry probe returns 401 against a valid-looking DSN | US-vs-EU region mismatch | Confirm DSN host: `*.ingest.us.sentry.io` vs `*.ingest.de.sentry.io`. Re-issue from the correct org. |
| PagerDuty probe returns 202 but no incident appears | Integration key bound to a different service, or service paused | Open the service → Integrations tab → confirm the key matches the one in `.env.local`. Unpause if paused. |
| Opsgenie probe returns 422 "team not found" | Team name typo or team scoped to a different region | Re-check team name verbatim; verify `OPSGENIE_REGION` matches the team's region. |
| Slack webhook returns 404 | Webhook revoked (app uninstalled, channel deleted, URL rotated) | Re-issue the webhook in Slack. Webhooks expire silently when the parent app is uninstalled. |
| Splunk HEC returns 403 "token disabled" | Token disabled or index ACL rejected the source | Re-enable token; confirm the token's allowed indexes include your target. |
| First burst of events rate-limited | SaaS first-write throttle (Datadog, Sentry both do this on cold accounts) | Backoff per the runbook's retry table; wait 60s, retry once. If sustained, file a SaaS-side ticket. |
| Verify passes but no human sees the alert | Notification routing not configured | Each runbook has a "post-setup wiring" section — escalation policies, channel routes, on-call rotations. Verify checks delivery to SaaS; routing-to-human is separate. |

If a failure mode isn't in this table, add it to `state/operator-deviations.md`. The next operator should not rediscover it.

---

## 5. Production rollout cadence

| Day | Stage | Action |
|-----|-------|--------|
| Day 1 | dev + staging | Complete steps 1–30 above. Both environments green on `verify-all.sh`. |
| Day 7 | prod canary | Enable for 1% of production traffic. Watch the six integrations' dashboards for 24h. Roll back if any integration silently drops events. |
| Day 14 | full prod rollout | Enable for 100% of production traffic. Run `verify-all.sh` daily for the first week. |
| Day 30 | first month-end audit | Reconcile event counts: what the app emitted vs what each SaaS received. Discrepancies > 1% are investigated. |

Rollback path at each stage: revert the feature flag (`OPERATOR_WIRING_PROD_ENABLED=0`), keep creds in place. Do not delete creds during rollback — rollback should be a one-flag operation, not a multi-step teardown.

---

## 6. Day-of-rollout incident response

If `verify-all.sh` fails post-go-live or an integration silently stops delivering:

1. **Do not delete creds.** Even broken creds are evidence.
2. **Preserve logs.** Snapshot the last 1h of integration logs to `state/incidents/<YYYYMMDD-HHMM>/`. Include the failing `verify-all.sh` output verbatim.
3. **Roll back the flag.** `OPERATOR_WIRING_PROD_ENABLED=0` if a feature flag controls the path; otherwise revert to the prior release tag.
4. **Escalate.** Page the integration owner per the on-call rotation in `setup-runbooks/<integration>.md` § Owner. If multiple integrations fail simultaneously, that's a substrate issue (network, DNS, proxy) — escalate to platform on-call, not per integration.
5. **Communicate.** One-line update to the operations channel: integration, observed symptom, action taken, ETA. Don't speculate on root cause until logs are read.
6. **After recovery.** Append a post-mortem entry to `state/incidents/<id>/post-mortem.md`. Update § 4 of this doc with the failure mode if it's novel.

Rollback is the default. Investigation happens after the flag is flipped, never instead of flipping it.

---

## 7. Ongoing maintenance

| Cadence | Task |
|---------|------|
| Daily (first 14 days post-rollout) | `verify-all.sh` runs on cron. Failures page the operator. |
| Weekly (steady state) | `verify-all.sh` on cron. Failures open a low-priority ticket. |
| Monthly | Reconcile event-count drift between app and each SaaS. Document drift > 1%. |
| Quarterly | Rotate every credential. Keep the old cred active for 24h overlap, swap `.env.local`, re-verify, then revoke the old cred at the SaaS side. |
| Quarterly | Dependabot review on the OTLP collector and any SaaS SDK pinned in `operator-wiring-2026-05/`. Bump minor versions; pin major versions until a manual review. |
| As-needed | When a SaaS changes API endpoints (Datadog has done this; PagerDuty deprecated v1 events), update the runbook and bump the verify script. |

Drift detection: `verify-all.sh` on cron is the cheapest cross-session sanity check the system has. Treat its failures as first-class incidents, not noise.

---

## Closing note

If you finish Day-1 and any integration is yellow or unverified, do not declare done. The honest-numbers contract here: green means green, and partial-green is HOLD. The next operator inherits exactly what this one leaves behind — leave it in a state you'd want to inherit.
