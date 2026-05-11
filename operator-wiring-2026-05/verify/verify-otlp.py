#!/usr/bin/env python3
"""verify-otlp.py — send a synthetic OTLP/HTTP-JSON span to a collector and confirm 200.

Usage:
  verify-otlp.py <ENDPOINT> <API_KEY> [--header-name DD-API-KEY] [--no-auth]

Examples:
  verify-otlp.py https://trace.agent.datadoghq.com $DD_API_KEY
  verify-otlp.py https://ingest.us0.signalfx.com/v2/trace/otlp $SPLUNK_TOKEN --header-name X-SF-Token
  verify-otlp.py http://localhost:4318 --no-auth

Exit codes:
  0 = HTTP 200/202; manual UI confirmation still required
  1 = missing creds (clear stderr message)
  2 = HTTP non-2xx
  3 = network / DNS / TLS failure
"""

from __future__ import annotations

import argparse
import json
import random
import sys
import time
import urllib.error
import urllib.request
import uuid


def _hex(n_bytes: int) -> str:
    return "".join(f"{random.randint(0, 255):02x}" for _ in range(n_bytes))


def build_payload(service: str) -> dict:
    """Build a minimal OTLP/HTTP-JSON traces payload (one span)."""
    now_ns = int(time.time() * 1_000_000_000)
    trace_id = _hex(16)
    span_id = _hex(8)
    return {
        "resourceSpans": [
            {
                "resource": {
                    "attributes": [
                        {"key": "service.name", "value": {"stringValue": service}},
                        {"key": "service.version", "value": {"stringValue": "verify-otlp/1.0"}},
                        {"key": "deployment.environment", "value": {"stringValue": "verify"}},
                    ]
                },
                "scopeSpans": [
                    {
                        "scope": {"name": "operator-wiring-verify"},
                        "spans": [
                            {
                                "traceId": trace_id,
                                "spanId": span_id,
                                "name": "verify.synthetic",
                                "kind": 1,  # SPAN_KIND_INTERNAL
                                "startTimeUnixNano": str(now_ns),
                                "endTimeUnixNano": str(now_ns + 1_000_000),
                                "attributes": [
                                    {
                                        "key": "verify.id",
                                        "value": {"stringValue": str(uuid.uuid4())},
                                    },
                                    {
                                        "key": "verify.note",
                                        "value": {
                                            "stringValue": "synthetic span from operator-wiring verify-otlp.py"
                                        },
                                    },
                                ],
                                "status": {"code": 1},  # OK
                            }
                        ],
                    }
                ],
            }
        ],
    }, trace_id


def send(endpoint: str, payload: dict, headers: dict, timeout: float = 10.0) -> tuple[int, str]:
    url = endpoint.rstrip("/") + "/v1/traces" if not endpoint.endswith("/v1/traces") and "/v" not in endpoint.rsplit("/", 1)[-1] else endpoint
    body = json.dumps(payload).encode("utf-8")
    base = {"Content-Type": "application/json", "User-Agent": "operator-wiring-verify/1.0"}
    base.update(headers)
    req = urllib.request.Request(url, data=body, headers=base, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read(500).decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read(500).decode("utf-8", errors="replace") if e.fp else ""
    except urllib.error.URLError as e:
        raise RuntimeError(f"network error: {e.reason}") from e


def main() -> int:
    p = argparse.ArgumentParser(description="Send a synthetic OTLP span to a collector.")
    p.add_argument("endpoint", help="OTLP/HTTP endpoint, e.g. https://trace.agent.datadoghq.com")
    p.add_argument("api_key", nargs="?", default=None, help="API key / token (omit with --no-auth)")
    p.add_argument("--header-name", default="DD-API-KEY", help="auth header name (default DD-API-KEY)")
    p.add_argument("--no-auth", action="store_true", help="skip auth header (for local collectors)")
    p.add_argument("--service", default="enchanter-agent-foundations", help="service.name attribute")
    args = p.parse_args()

    if not args.no_auth and not args.api_key:
        print("[verify-otlp] FAIL — missing API key. Pass it as second arg or use --no-auth.", file=sys.stderr)
        print("[verify-otlp] e.g.: verify-otlp.py https://trace.agent.datadoghq.com $DD_API_KEY", file=sys.stderr)
        return 1

    print(f"[verify-otlp] target={args.endpoint}")
    payload, trace_id = build_payload(args.service)
    print(f"[verify-otlp] sending synthetic span trace_id={trace_id}")

    headers = {}
    if not args.no_auth:
        headers[args.header_name] = args.api_key

    try:
        status, body = send(args.endpoint, payload, headers)
    except RuntimeError as e:
        print(f"[verify-otlp] FAIL — {e}", file=sys.stderr)
        return 3

    print(f"[verify-otlp] HTTP {status}")
    if 200 <= status < 300:
        print("[verify-otlp] PASS — span accepted by collector")
        print(f"[verify-otlp] Manual: confirm span service={args.service} op=verify.synthetic visible in your APM UI within 60s.")
        return 0

    snippet = body.strip().replace("\n", " ")[:200]
    print(f"[verify-otlp] FAIL — non-2xx; body: {snippet}", file=sys.stderr)
    if status in (401, 403):
        print("[verify-otlp] hint: check API key validity + header name matches backend (DD-API-KEY vs X-SF-Token).", file=sys.stderr)
    elif status == 404:
        print("[verify-otlp] hint: endpoint path may be wrong; some backends want /v1/traces appended.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
