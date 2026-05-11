# Operator Setup Checklist — agent-foundations wiring

Goal: take the kit from "files on disk" to "live integration" in one focused session per integration. Run top-to-bottom once; check each box as you go.

Time budget: ~1 day total if all six integrations go live. ~15 min per integration plus 30 min for cross-cutting steps.

---

## Phase 0 — Prerequisites (10 min)

1. [ ] Verify `python3 --version` reports >= 3.9.
   - Expected: `Python 3.9.x` or higher.
   - If fails: install python3 from your package manager; this kit uses stdlib only.

2. [ ] Clone or copy the kit somewhere agents can run it. Confirm:
   ```
   ls operator-wiring-2026-05/
   ```
   - Expected: `README.md`, `verify/`, `mock-endpoints/`, `setup-runbooks/`, `config-validator.py`, `setup-checklist.md`.

3. [ ] Make scripts executable (Unix/WSL only):
   ```
   chmod +x operator-wiring-2026-05/verify/*.sh operator-wiring-2026-05/mock-endpoints/*.sh
   ```

4. [ ] Confirm egress allow-list includes (if operator runs behind a corporate proxy):
   - `*.datadoghq.com` (or your DD region)
   - `*.ingest.sentry.io`
   - `events.pagerduty.com`
   - `api.opsgenie.com` (or eu region)
   - `hooks.slack.com`
   - `*.signalfx.com` (if using Splunk)

5. [ ] Decide which integrations are in scope for this rollout. Suggested minimum: PagerDuty (or Opsgenie) + Slack + one tracing backend (DD or Sentry).

---

## Phase 1 — Smoke-test the mocks (10 min)

Before touching real creds, confirm the kit itself works.

6. [ ] Start the mocks:
   ```
   ./operator-wiring-2026-05/mock-endpoints/run-mocks.sh start
   ```
   - Expected: four "pid=... OK" lines.
   - Troubleshooting: if a port collides, edit `run-mocks.sh` to use different ports, or kill the conflicting process.

7. [ ] Send a synthetic OTLP span at the mock collector:
   ```
   python3 operator-wiring-2026-05/verify/verify-otlp.py http://localhost:4318 --no-auth
   ```
   - Expected: `HTTP 200`, `PASS — span accepted by collector`.

8. [ ] Send a synthetic PagerDuty event at the mock:
   ```
   python3 operator-wiring-2026-05/verify/verify-pager.py http://localhost:8123/v2/enqueue mock-key-1234
   ```
   - Expected: `HTTP 202`, `PASS — event accepted`.

9. [ ] Send a synthetic Slack message at the mock:
   ```
   python3 operator-wiring-2026-05/verify/verify-slack.py http://localhost:8124/services/Tmock/Bmock/mocksecret
   ```
   - Expected: `HTTP 200`, response body `ok`, `PASS — posted to channel`.

10. [ ] Stop the mocks (production verifies don't need them):
    ```
    ./operator-wiring-2026-05/mock-endpoints/run-mocks.sh stop
    ```

If steps 6–10 all pass, the kit itself is healthy. Proceed to real-cred wiring.

---

## Phase 2 — Per-integration wiring

For each integration: open the runbook, follow it end-to-end, run the verify, confirm in the UI.

### Datadog OTLP (15 min)

11. [ ] Read `setup-runbooks/datadog-otlp.md`.
12. [ ] Generate API key in Datadog UI; store in secret manager.
13. [ ] Set env vars: `DD_API_KEY`, `DD_SITE`, `OTEL_EXPORTER_OTLP_ENDPOINT`, `OTEL_EXPORTER_OTLP_HEADERS`.
14. [ ] Run `python3 verify/verify-otlp.py "$OTEL_EXPORTER_OTLP_ENDPOINT" "$DD_API_KEY"`.
    - Expected: `HTTP 200` then `PASS`.
    - If FAIL: see runbook troubleshooting table.
15. [ ] Open Datadog APM → filter `service:enchanter-agent-foundations` → confirm synthetic span visible.

### Sentry (10 min)

16. [ ] Read `setup-runbooks/sentry-llm-monitoring.md`.
17. [ ] Create Sentry project (AI / Python); copy DSN.
18. [ ] Set env var `SENTRY_DSN`.
19. [ ] Run `python3 verify/verify-sentry.py "$SENTRY_DSN"`.
    - Expected: `HTTP 200`, `PASS`.
20. [ ] Open Sentry Issues → search `verify.synthetic` → confirm event visible.

### PagerDuty (10 min)

21. [ ] Read `setup-runbooks/pagerduty-events-v2.md`.
22. [ ] Create Events API v2 integration on target service; copy integration key.
23. [ ] Set env vars `PD_INTEGRATION_KEY`, `PD_EVENTS_URL`.
24. [ ] Run `python3 verify/verify-pager.py "$PD_EVENTS_URL" "$PD_INTEGRATION_KEY"`.
    - Expected: `HTTP 202`, `PASS`.
25. [ ] Open PagerDuty incidents list → confirm synthetic incident visible → **resolve it manually**.

### Opsgenie (10 min) [alternative to PagerDuty]

26. [ ] Read `setup-runbooks/opsgenie-events.md`.
27. [ ] Create API integration on target team; copy key; identify region.
28. [ ] Set env vars `OPSGENIE_API_KEY`, `OPSGENIE_URL`.
29. [ ] Run `python3 verify/verify-pager.py "$OPSGENIE_URL" "$OPSGENIE_API_KEY" --provider opsgenie`.
    - Expected: `HTTP 202`, `PASS`.
30. [ ] Open Opsgenie alert list → confirm synthetic alert visible → **close it manually**.

### Slack (5 min)

31. [ ] Read `setup-runbooks/slack-webhook.md`.
32. [ ] Create Slack app + incoming webhook on target channel; copy webhook URL.
33. [ ] Set env var `SLACK_WEBHOOK_URL`.
34. [ ] Run `python3 verify/verify-slack.py "$SLACK_WEBHOOK_URL"`.
    - Expected: `HTTP 200`, body `ok`, `PASS`.
35. [ ] Open the channel → confirm synthetic advisory visible.

### Splunk OTLP (15 min) [optional, alt to Datadog]

36. [ ] Read `setup-runbooks/splunk-otlp.md`.
37. [ ] Create INGEST-scoped access token; identify realm.
38. [ ] Set env vars per runbook.
39. [ ] Run `python3 verify/verify-otlp.py "$SPLUNK_OTLP_ENDPOINT" "$SPLUNK_ACCESS_TOKEN" --header-name X-SF-Token`.
    - Expected: `HTTP 200`, `PASS`.
40. [ ] Open Splunk APM → filter on service → confirm visible.

---

## Phase 3 — Cross-cutting validation (15 min)

41. [ ] Run the master verify with all env vars set:
    ```
    bash operator-wiring-2026-05/verify/verify-all.sh
    ```
    - Expected: green `[ OK ]` per attempted integration; any `[FAIL]` indicates a misconfiguration in that integration.

42. [ ] Validate operator config files (paging + OTEL):
    ```
    python3 operator-wiring-2026-05/config-validator.py paging-config.json otel-config.yaml --all
    ```
    - Expected: `OK` per file, or specific findings to fix.

43. [ ] Confirm all secrets live in the secret manager, not on disk:
    ```
    grep -r "sk-" /path/to/agent-foundations/  # adapt to your secret prefixes
    grep -r "events.pagerduty.com/v2" /path/to/agent-foundations/  # ensure no inline keys
    ```
    - Expected: no hits, or only documentation hits in `setup-runbooks/`.

44. [ ] Rotate one key as a fire drill:
    - Pick one integration, regenerate its key, update secret manager, re-run verify.
    - Confirms rotation procedure works.

45. [ ] Document the live config in your runbook:
    - Which DD site, which Sentry project, which PD service, which Slack channel.
    - Where secrets live.
    - On-call escalation policy.

---

## Phase 4 — Handoff to agent-foundations runtime (10 min)

46. [ ] Update agent-foundations' `paging-config.json` / `otel-config.yaml` with the live endpoints and references to secret-manager paths (not raw values).

47. [ ] Restart agent-foundations runtime with the new config.

48. [ ] Trigger one real low-severity advisory (e.g., a synthetic MEDIUM event from inside the runtime, not the verify scripts) and confirm:
    - [ ] PagerDuty/Opsgenie incident visible (and auto-resolves per dedup_key)
    - [ ] Slack post visible
    - [ ] Span visible in tracing backend
    - [ ] Sentry event visible

49. [ ] Set 90-day rotation calendar reminders for each key.

50. [ ] Capture screenshots of the four backends showing the synthetic event for the runbook archive.

---

## Done

When all 50 boxes are checked, agent-foundations is wired. From this point on, integration changes are config edits + a verify run — no kit code changes needed.

If a step fails: re-read the relevant runbook's "Troubleshooting" table. Failures in this kit are almost always (1) wrong endpoint for region, (2) wrong header name, (3) key with insufficient scope, or (4) egress blocked.
