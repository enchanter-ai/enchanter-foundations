# Playbook — CC7.2 Anomaly detection

- **Control ID:** CC7.2
- **Control description:** The entity monitors system components and the operation of those components for anomalies that are indicative of malicious acts, natural disasters, and errors affecting the entity's ability to meet its objectives.
- **Evidence-collection mechanism:** Daily tail of `hydra/plugins/audit-trail/state/log.jsonl` (HMAC-chained tamper-evident log) plus hash of inference-engine catalog (SPRT-elevated anomaly patterns).
- **Producer (today):** `hydra/plugins/audit-trail/`, `wixie/plugins/inference-engine/`. Future: `naga/naga-observe` drift detection.
- **Retention rule:** 7 years.
- **Who reviews:** Repo maintainer weekly.
- **Escalation path:** HMAC chain break → tamper investigation. **GAP:** F-021/F-024 OTLP exporter not yet shipped.
- **Type II evidence shape:** Continuous tamper-evident log + SPRT catalog rotations across the window.
- **External dependency:** Future OTLP collector (customer-side or hosted) for telemetry export.
