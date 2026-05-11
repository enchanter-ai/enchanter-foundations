#!/usr/bin/env python3
"""mock-pagerduty.py — fake PagerDuty Events v2 endpoint on localhost:8123.

Accepts POST /v2/enqueue. Validates required fields per Events v2 spec.
Returns 202 + {status, message, dedup_key} on valid payload, 400 on invalid.

Run:
  python3 mock-pagerduty.py [--port 8123] [--host 127.0.0.1]
"""

from __future__ import annotations

import argparse
import datetime as dt
import http.server
import json
import sys
import uuid


REQUIRED_TOP = {"routing_key", "event_action"}
REQUIRED_PAYLOAD_FOR_TRIGGER = {"summary", "source", "severity"}
VALID_SEVERITY = {"critical", "error", "warning", "info"}
VALID_ACTION = {"trigger", "acknowledge", "resolve"}


class Handler(http.server.BaseHTTPRequestHandler):
    server_version = "MockPagerDuty/1.0"

    def log_message(self, fmt: str, *args) -> None:  # noqa: A003
        return

    def _now(self) -> str:
        return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")

    def _emit(self, msg: str) -> None:
        print(f"[{self._now()}] {msg}", flush=True)

    def _reply(self, status: int, obj: dict) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(obj).encode("utf-8"))

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/v2/enqueue":
            self._emit(f"POST {self.path} — 404")
            self._reply(404, {"status": "error", "message": "unknown path"})
            return

        length = int(self.headers.get("Content-Length", "0") or "0")
        body = self.rfile.read(length) if length else b""
        try:
            doc = json.loads(body)
        except json.JSONDecodeError:
            self._emit(f"POST {self.path} — 400 (json decode)")
            self._reply(400, {"status": "invalid event", "errors": ["body is not valid JSON"]})
            return

        errors = []
        missing = REQUIRED_TOP - set(doc.keys())
        if missing:
            errors.append(f"missing top-level fields: {sorted(missing)}")

        action = doc.get("event_action")
        if action and action not in VALID_ACTION:
            errors.append(f"event_action must be one of {sorted(VALID_ACTION)}")

        dedup_key = doc.get("dedup_key") or f"mock-{uuid.uuid4()}"

        if action == "trigger":
            payload = doc.get("payload") or {}
            missing_p = REQUIRED_PAYLOAD_FOR_TRIGGER - set(payload.keys())
            if missing_p:
                errors.append(f"payload missing fields: {sorted(missing_p)}")
            sev = payload.get("severity")
            if sev and sev not in VALID_SEVERITY:
                errors.append(f"payload.severity must be one of {sorted(VALID_SEVERITY)}")
            summary = payload.get("summary", "")
            if isinstance(summary, str) and len(summary) > 1024:
                errors.append("payload.summary exceeds 1024 chars")

        if action in ("resolve", "acknowledge") and not doc.get("dedup_key"):
            errors.append(f"event_action={action} requires dedup_key")

        if errors:
            self._emit(f"POST {self.path} — 400 errors={errors}")
            self._reply(400, {"status": "invalid event", "errors": errors})
            return

        self._emit(
            f"POST {self.path} — 202 action={action} "
            f"dedup_key={dedup_key} routing_key=****{str(doc.get('routing_key',''))[-4:]}"
        )
        self._reply(202, {
            "status": "success",
            "message": "Event processed",
            "dedup_key": dedup_key,
        })

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/healthz":
            self._reply(200, {"status": "ok"})
            return
        self._reply(404, {"status": "error", "message": "unknown path"})


def main() -> int:
    p = argparse.ArgumentParser(description="mock PagerDuty Events v2")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8123)
    args = p.parse_args()

    srv = http.server.ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"[mock-pagerduty] listening on http://{args.host}:{args.port}/v2/enqueue", flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("[mock-pagerduty] stopping", flush=True)
        srv.shutdown()
    return 0


if __name__ == "__main__":
    sys.exit(main())
