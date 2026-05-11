#!/usr/bin/env python3
"""mock-opsgenie.py — fake Opsgenie Alerts v2 endpoint on localhost:8125.

Accepts POST /v2/alerts (create), POST /v2/alerts/<alias>/close (close).
Validates Authorization: GenieKey header, required fields, priority enum.
Returns 202 + {requestId, result} per Opsgenie convention.

Run:
  python3 mock-opsgenie.py [--port 8125] [--host 127.0.0.1]
"""

from __future__ import annotations

import argparse
import datetime as dt
import http.server
import json
import sys
import uuid


VALID_PRIORITY = {"P1", "P2", "P3", "P4", "P5"}


class Handler(http.server.BaseHTTPRequestHandler):
    server_version = "MockOpsgenie/1.0"

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

    def _check_auth(self) -> str | None:
        auth = self.headers.get("Authorization", "")
        if not auth.startswith("GenieKey "):
            return None
        return auth[len("GenieKey ") :].strip() or None

    def do_POST(self) -> None:  # noqa: N802
        token = self._check_auth()
        if not token:
            self._emit(f"POST {self.path} — 401 (no GenieKey)")
            self._reply(401, {"message": "missing or malformed Authorization: GenieKey"})
            return

        length = int(self.headers.get("Content-Length", "0") or "0")
        body = self.rfile.read(length) if length else b""

        try:
            doc = json.loads(body) if body else {}
        except json.JSONDecodeError:
            self._emit(f"POST {self.path} — 400 (json decode)")
            self._reply(400, {"message": "body is not valid JSON"})
            return

        # close path: /v2/alerts/<alias>/close
        parts = self.path.split("?")[0].strip("/").split("/")
        if len(parts) == 4 and parts[0] == "v2" and parts[1] == "alerts" and parts[3] == "close":
            alias = parts[2]
            self._emit(f"POST {self.path} — 202 close alias={alias}")
            self._reply(202, {
                "result": "Request will be processed",
                "took": 0.001,
                "requestId": str(uuid.uuid4()),
            })
            return

        # create path: /v2/alerts
        if self.path.split("?")[0] != "/v2/alerts":
            self._emit(f"POST {self.path} — 404")
            self._reply(404, {"message": "unknown path"})
            return

        errors = []
        if not doc.get("message"):
            errors.append("message is required")
        elif len(doc["message"]) > 130:
            errors.append("message exceeds 130 chars")

        prio = doc.get("priority", "P3")
        if prio not in VALID_PRIORITY:
            errors.append(f"priority must be one of {sorted(VALID_PRIORITY)}")

        if errors:
            self._emit(f"POST {self.path} — 422 errors={errors}")
            self._reply(422, {"message": "validation failed", "errors": errors})
            return

        alias = doc.get("alias") or f"mock-{uuid.uuid4()}"
        self._emit(
            f"POST {self.path} — 202 create alias={alias} priority={prio} "
            f"token=****{token[-4:] if len(token) > 4 else '****'}"
        )
        self._reply(202, {
            "result": "Request will be processed",
            "took": 0.002,
            "requestId": str(uuid.uuid4()),
        })

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/healthz":
            self._reply(200, {"status": "ok"})
            return
        self._reply(404, {"message": "unknown path"})


def main() -> int:
    p = argparse.ArgumentParser(description="mock Opsgenie Alerts v2")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8125)
    args = p.parse_args()

    srv = http.server.ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"[mock-opsgenie] listening on http://{args.host}:{args.port}/v2/alerts", flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("[mock-opsgenie] stopping", flush=True)
        srv.shutdown()
    return 0


if __name__ == "__main__":
    sys.exit(main())
