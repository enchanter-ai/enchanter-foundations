#!/usr/bin/env python3
"""verify-pager.py — send a synthetic event to PagerDuty Events v2 or Opsgenie Alerts v2.

Usage:
  verify-pager.py <WEBHOOK_URL> <KEY> [--provider pagerduty|opsgenie] [--auto-resolve]

Examples:
  verify-pager.py https://events.pagerduty.com/v2/enqueue $PD_INTEGRATION_KEY
  verify-pager.py https://api.opsgenie.com/v2/alerts $OPSGENIE_API_KEY --provider opsgenie

Exit codes:
  0 = HTTP 2xx accepted
  1 = missing creds
  2 = HTTP non-2xx
  3 = network failure
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import urllib.error
import urllib.request
import uuid


def pd_payload(routing_key: str, dedup_key: str) -> dict:
    return {
        "routing_key": routing_key,
        "event_action": "trigger",
        "dedup_key": dedup_key,
        "payload": {
            "summary": "verify.synthetic — agent-foundations integration check",
            "source": "enchanter-agent-foundations",
            "severity": "warning",
            "timestamp": dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z"),
            "component": "operator-wiring",
            "group": "verify",
            "class": "synthetic",
            "custom_details": {
                "note": "This is a synthetic event sent by verify-pager.py. Resolve manually after confirming.",
                "verify_id": str(uuid.uuid4()),
            },
        },
    }


def pd_resolve(routing_key: str, dedup_key: str) -> dict:
    return {
        "routing_key": routing_key,
        "event_action": "resolve",
        "dedup_key": dedup_key,
    }


def og_payload(alias: str) -> dict:
    return {
        "message": "verify.synthetic — agent-foundations integration check",
        "alias": alias,
        "description": "Synthetic alert from verify-pager.py. Close manually after confirming.",
        "priority": "P5",
        "source": "enchanter-agent-foundations",
        "tags": ["agent-foundations", "verify", "synthetic"],
        "details": {"verify_id": str(uuid.uuid4())},
    }


def http_post_json(url: str, payload: dict, headers: dict, timeout: float = 10.0) -> tuple[int, str]:
    body = json.dumps(payload).encode("utf-8")
    base = {"Content-Type": "application/json", "User-Agent": "operator-wiring-verify/1.0"}
    base.update(headers)
    req = urllib.request.Request(url, data=body, headers=base, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read(2000).decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, (e.read(2000).decode("utf-8", errors="replace") if e.fp else "")
    except urllib.error.URLError as e:
        raise RuntimeError(f"network error: {e.reason}") from e


def main() -> int:
    p = argparse.ArgumentParser(description="Send a synthetic event to PagerDuty or Opsgenie.")
    p.add_argument("url", help="provider events URL")
    p.add_argument("key", nargs="?", default=None, help="integration/API key")
    p.add_argument("--provider", choices=("pagerduty", "opsgenie"), default="pagerduty")
    p.add_argument("--auto-resolve", action="store_true", help="resolve the synthetic event immediately after triggering")
    args = p.parse_args()

    if not args.key:
        print(f"[verify-pager] FAIL — missing key. Pass it as second arg.", file=sys.stderr)
        print(f"[verify-pager] e.g.: verify-pager.py {args.url} $YOUR_KEY", file=sys.stderr)
        return 1

    dedup = f"verify-synthetic-{uuid.uuid4()}"
    print(f"[verify-pager] target={args.url} ({args.provider})")
    print(f"[verify-pager] sending synthetic event dedup/alias={dedup}")

    if args.provider == "pagerduty":
        payload = pd_payload(args.key, dedup)
        headers = {}
    else:
        payload = og_payload(dedup)
        headers = {"Authorization": f"GenieKey {args.key}"}

    try:
        status, body = http_post_json(args.url, payload, headers)
    except RuntimeError as e:
        print(f"[verify-pager] FAIL — {e}", file=sys.stderr)
        return 3

    print(f"[verify-pager] HTTP {status}")
    if 200 <= status < 300:
        print("[verify-pager] PASS — event accepted")
        snippet = body.strip().replace("\n", " ")[:200]
        if snippet:
            print(f"[verify-pager] response: {snippet}")
        if args.provider == "pagerduty":
            print("[verify-pager] Manual: confirm incident visible in PagerDuty incident list, then resolve it.")
            print("[verify-pager]         (or pass --auto-resolve to close it now)")
        else:
            print("[verify-pager] Manual: confirm alert visible in Opsgenie alert list, then close it.")

        if args.auto_resolve:
            if args.provider == "pagerduty":
                print("[verify-pager] auto-resolving via dedup_key…")
                rstatus, _ = http_post_json(args.url, pd_resolve(args.key, dedup), {})
                print(f"[verify-pager] resolve HTTP {rstatus}")
            else:
                rurl = args.url.rstrip("/") + f"/{dedup}/close?identifierType=alias"
                rstatus, _ = http_post_json(rurl, {"source": "verify-pager.py"}, headers)
                print(f"[verify-pager] close HTTP {rstatus}")
        return 0

    snippet = body.strip().replace("\n", " ")[:300]
    print(f"[verify-pager] FAIL — non-2xx; body: {snippet}", file=sys.stderr)
    if status in (401, 403):
        if args.provider == "opsgenie":
            print("[verify-pager] hint: Opsgenie requires 'Authorization: GenieKey <key>' (not Bearer).", file=sys.stderr)
        else:
            print("[verify-pager] hint: PagerDuty Events v2 puts the key in JSON body as 'routing_key', not in a header.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
