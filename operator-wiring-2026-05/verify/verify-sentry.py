#!/usr/bin/env python3
"""verify-sentry.py — send a synthetic LLM-shaped event to Sentry via the envelope endpoint.

Usage:
  verify-sentry.py <DSN>

DSN shape:
  https://<public_key>@<host>/<project_id>

Exit codes:
  0 = HTTP 2xx accepted
  1 = missing/malformed DSN
  2 = HTTP non-2xx
  3 = network failure
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid


def parse_dsn(dsn: str) -> tuple[str, str, str, str]:
    """Return (scheme, host, public_key, project_id)."""
    p = urllib.parse.urlparse(dsn)
    if not p.scheme or not p.username or not p.hostname or not p.path:
        raise ValueError("DSN must look like https://<key>@<host>/<project_id>")
    project_id = p.path.strip("/")
    if not project_id:
        raise ValueError("DSN missing project_id")
    return p.scheme, p.hostname, p.username, project_id


def envelope_event(event_id: str) -> bytes:
    """Build an envelope with one synthetic event."""
    now = dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")
    sent_at = now
    event = {
        "event_id": event_id.replace("-", ""),
        "timestamp": time.time(),
        "platform": "python",
        "level": "info",
        "logger": "operator-wiring.verify",
        "transaction": "verify.synthetic",
        "environment": "verify",
        "release": "operator-wiring@1.0.0",
        "tags": {"verify": "true", "synthetic": "true"},
        "extra": {
            "note": "Synthetic event sent by verify-sentry.py from agent-foundations operator-wiring kit.",
        },
        "message": {"formatted": "verify.synthetic — agent-foundations integration check"},
        # AI-monitoring shaped breadcrumb
        "breadcrumbs": {
            "values": [
                {
                    "type": "ai",
                    "category": "ai.chat",
                    "timestamp": time.time(),
                    "data": {
                        "ai.model_id": "synthetic-model",
                        "ai.prompt_tokens": 1,
                        "ai.completion_tokens": 1,
                        "ai.total_tokens": 2,
                    },
                    "message": "synthetic AI call",
                }
            ]
        },
    }
    header = {"event_id": event["event_id"], "sent_at": sent_at}
    item_header = {"type": "event", "content_type": "application/json"}
    item_body = json.dumps(event).encode("utf-8")
    item_header["length"] = len(item_body)
    parts = [
        json.dumps(header).encode("utf-8"),
        b"\n",
        json.dumps(item_header).encode("utf-8"),
        b"\n",
        item_body,
        b"\n",
    ]
    return b"".join(parts)


def main() -> int:
    p = argparse.ArgumentParser(description="Send a synthetic Sentry envelope.")
    p.add_argument("dsn", nargs="?", default=None, help="Sentry DSN")
    args = p.parse_args()

    if not args.dsn:
        print("[verify-sentry] FAIL — missing DSN. Pass as first arg or set SENTRY_DSN env.", file=sys.stderr)
        return 1

    try:
        scheme, host, public_key, project_id = parse_dsn(args.dsn)
    except ValueError as e:
        print(f"[verify-sentry] FAIL — bad DSN: {e}", file=sys.stderr)
        return 1

    print(f"[verify-sentry] dsn host={host} project={project_id}")
    event_id = str(uuid.uuid4())
    print(f"[verify-sentry] sending synthetic LLM trace event_id={event_id}")

    url = f"{scheme}://{host}/api/{project_id}/envelope/"
    body = envelope_event(event_id)
    sentry_auth = (
        "Sentry "
        f"sentry_version=7, "
        f"sentry_client=operator-wiring-verify/1.0, "
        f"sentry_timestamp={int(time.time())}, "
        f"sentry_key={public_key}"
    )
    headers = {
        "Content-Type": "application/x-sentry-envelope",
        "X-Sentry-Auth": sentry_auth,
        "User-Agent": "operator-wiring-verify/1.0",
    }
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=10.0) as resp:
            status = resp.status
            response_body = resp.read(500).decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        status = e.code
        response_body = (e.read(500).decode("utf-8", errors="replace") if e.fp else "")
    except urllib.error.URLError as e:
        print(f"[verify-sentry] FAIL — network error: {e.reason}", file=sys.stderr)
        return 3

    print(f"[verify-sentry] HTTP {status}")
    if 200 <= status < 300:
        print("[verify-sentry] PASS — event accepted by Sentry")
        snippet = response_body.strip().replace("\n", " ")[:200]
        if snippet:
            print(f"[verify-sentry] response: {snippet}")
        print(f"[verify-sentry] Manual: confirm event id={event_id.replace('-', '')} visible in Sentry within 30s.")
        return 0

    snippet = response_body.strip().replace("\n", " ")[:300]
    print(f"[verify-sentry] FAIL — non-2xx; body: {snippet}", file=sys.stderr)
    if status == 401:
        print("[verify-sentry] hint: public_key in DSN may be wrong/disabled. Re-copy from Project → Client Keys.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
