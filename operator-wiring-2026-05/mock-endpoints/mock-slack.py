#!/usr/bin/env python3
"""mock-slack.py — fake Slack incoming-webhook receiver on localhost:8124.

Accepts POST /services/<team>/<channel>/<secret>. Validates Block Kit shape
(at minimum: 'text' or 'blocks'). Returns 200 + body 'ok' on success.

Run:
  python3 mock-slack.py [--port 8124] [--host 127.0.0.1]

Point a client at:
  http://localhost:8124/services/Tmock/Bmock/mocksecret
"""

from __future__ import annotations

import argparse
import datetime as dt
import http.server
import json
import sys


VALID_BLOCK_TYPES = {
    "actions", "context", "divider", "header", "image", "input", "section",
}


class Handler(http.server.BaseHTTPRequestHandler):
    server_version = "MockSlack/1.0"

    def log_message(self, fmt: str, *args) -> None:  # noqa: A003
        return

    def _now(self) -> str:
        return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")

    def _emit(self, msg: str) -> None:
        print(f"[{self._now()}] {msg}", flush=True)

    def _reply_text(self, status: int, body: str) -> None:
        encoded = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_POST(self) -> None:  # noqa: N802
        if not self.path.startswith("/services/"):
            self._emit(f"POST {self.path} — 404")
            self._reply_text(404, "invalid_path")
            return

        parts = self.path.strip("/").split("/")
        if len(parts) != 4:
            self._emit(f"POST {self.path} — 404 (bad webhook shape)")
            self._reply_text(404, "invalid_token")
            return

        length = int(self.headers.get("Content-Length", "0") or "0")
        body = self.rfile.read(length) if length else b""
        try:
            doc = json.loads(body)
        except json.JSONDecodeError:
            self._emit(f"POST {self.path} — 400 (json decode)")
            self._reply_text(400, "invalid_payload")
            return

        if "text" not in doc and "blocks" not in doc:
            self._emit(f"POST {self.path} — 400 (no text or blocks)")
            self._reply_text(400, "no_text")
            return

        blocks = doc.get("blocks") or []
        if not isinstance(blocks, list):
            self._emit(f"POST {self.path} — 400 (blocks not list)")
            self._reply_text(400, "invalid_blocks")
            return

        if len(blocks) > 50:
            self._emit(f"POST {self.path} — 400 (>50 blocks)")
            self._reply_text(400, "too_many_blocks")
            return

        for i, b in enumerate(blocks):
            if not isinstance(b, dict) or "type" not in b:
                self._emit(f"POST {self.path} — 400 (block[{i}] missing type)")
                self._reply_text(400, "invalid_blocks")
                return
            if b["type"] not in VALID_BLOCK_TYPES:
                self._emit(f"POST {self.path} — 400 (block[{i}] type={b['type']!r})")
                self._reply_text(400, "invalid_blocks")
                return

        text_preview = (doc.get("text") or "").replace("\n", " ")[:80]
        self._emit(
            f"POST {self.path} — 200 blocks={len(blocks)} text={text_preview!r}"
        )
        self._reply_text(200, "ok")

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/healthz":
            self._reply_text(200, "ok")
            return
        self._reply_text(404, "not_found")


def main() -> int:
    p = argparse.ArgumentParser(description="mock Slack incoming-webhook")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8124)
    args = p.parse_args()

    srv = http.server.ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"[mock-slack] listening on http://{args.host}:{args.port}/services/<t>/<b>/<s>", flush=True)
    print(f"[mock-slack] sample webhook: http://{args.host}:{args.port}/services/Tmock/Bmock/mocksecret", flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("[mock-slack] stopping", flush=True)
        srv.shutdown()
    return 0


if __name__ == "__main__":
    sys.exit(main())
