#!/usr/bin/env python3
"""mock-otlp-collector.py — minimal OTLP/HTTP-JSON collector on localhost:4318.

Accepts POST to /v1/traces, /v1/metrics, /v1/logs. Logs the request method, path,
auth header presence, payload size, and span/log structure. Replies 200 with an
empty partial-success body (per OTLP spec).

Run:
  python3 mock-otlp-collector.py [--port 4318] [--host 127.0.0.1]

Then point a client:
  curl -X POST http://localhost:4318/v1/traces \
    -H "Content-Type: application/json" \
    -d '{"resourceSpans":[]}'
"""

from __future__ import annotations

import argparse
import datetime as dt
import http.server
import json
import sys
import threading


class Handler(http.server.BaseHTTPRequestHandler):
    server_version = "MockOTLP/1.0"

    def log_message(self, fmt: str, *args) -> None:  # noqa: A003
        # silence default access log; we print our own
        return

    def _now(self) -> str:
        return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")

    def _emit(self, payload_summary: str) -> None:
        print(f"[{self._now()}] {self.command} {self.path} — {payload_summary}", flush=True)

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length", "0") or "0")
        body = self.rfile.read(length) if length else b""
        ctype = self.headers.get("Content-Type", "")
        auth_seen = []
        for h in ("Authorization", "DD-API-KEY", "X-SF-Token", "X-Sentry-Auth"):
            if h in self.headers:
                auth_seen.append(h)

        # try parse JSON for structure-aware log
        spans = logs = metrics = 0
        parsed_note = ""
        if "json" in ctype.lower() and body:
            try:
                doc = json.loads(body)
                for rs in doc.get("resourceSpans", []) or []:
                    for ss in rs.get("scopeSpans", []) or []:
                        spans += len(ss.get("spans", []) or [])
                for rl in doc.get("resourceLogs", []) or []:
                    for sl in rl.get("scopeLogs", []) or []:
                        logs += len(sl.get("logRecords", []) or [])
                for rm in doc.get("resourceMetrics", []) or []:
                    for sm in rm.get("scopeMetrics", []) or []:
                        metrics += len(sm.get("metrics", []) or [])
                parsed_note = f"spans={spans} logs={logs} metrics={metrics}"
            except json.JSONDecodeError as e:
                parsed_note = f"json-parse-error: {e}"
        elif body and "protobuf" in ctype.lower():
            parsed_note = "protobuf payload (not parsed by mock)"
        else:
            parsed_note = "empty or unknown content-type"

        self._emit(
            f"bytes={length} ctype={ctype or '?'} "
            f"auth={','.join(auth_seen) or 'none'} {parsed_note}"
        )

        if self.path not in ("/v1/traces", "/v1/metrics", "/v1/logs"):
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"error":"unknown path"}')
            return

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b"{}")

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/healthz":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"ok")
            return
        self.send_response(404)
        self.end_headers()


def main() -> int:
    p = argparse.ArgumentParser(description="mock OTLP/HTTP collector")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=4318)
    args = p.parse_args()

    srv = http.server.ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"[mock-otlp] listening on http://{args.host}:{args.port} (OTLP/HTTP-JSON)", flush=True)
    print("[mock-otlp] paths: /v1/traces /v1/metrics /v1/logs /healthz", flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("[mock-otlp] stopping", flush=True)
        srv.shutdown()
    return 0


if __name__ == "__main__":
    sys.exit(main())
