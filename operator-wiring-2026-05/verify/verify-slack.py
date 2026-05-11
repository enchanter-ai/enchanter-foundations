#!/usr/bin/env python3
"""verify-slack.py — post a synthetic Block Kit advisory to a Slack incoming webhook.

Usage:
  verify-slack.py <WEBHOOK_URL>

Exit codes:
  0 = HTTP 200 + response body "ok"
  1 = missing URL
  2 = HTTP non-2xx or body != "ok"
  3 = network failure
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
import uuid


def synthetic_payload() -> dict:
    advisory_id = str(uuid.uuid4())
    return {
        "text": "[verify.synthetic] agent-foundations operator-wiring integration check",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "[VERIFY] agent-foundations operator-wiring check",
                },
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": "*Severity*\nINFO (synthetic)"},
                    {"type": "mrkdwn", "text": "*Category*\nverify.synthetic"},
                    {"type": "mrkdwn", "text": "*Source*\nenchanter-agent-foundations"},
                    {"type": "mrkdwn", "text": "*Action*\nNone — synthetic, ignore."},
                ],
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"advisory_id: `{advisory_id}` · sent by `verify-slack.py`",
                    }
                ],
            },
        ],
    }


def main() -> int:
    p = argparse.ArgumentParser(description="Post a synthetic message to a Slack webhook.")
    p.add_argument("webhook_url", nargs="?", default=None, help="Slack incoming webhook URL")
    args = p.parse_args()

    if not args.webhook_url:
        print("[verify-slack] FAIL — missing webhook URL. Pass as first arg or set SLACK_WEBHOOK_URL.", file=sys.stderr)
        return 1

    # mask the secret half of the URL in output
    if args.webhook_url.startswith("https://hooks.slack.com/services/"):
        rest = args.webhook_url.split("/services/", 1)[1].split("/")
        masked = "https://hooks.slack.com/services/" + "/".join(rest[:2] + ["****"])
    else:
        masked = args.webhook_url
    print(f"[verify-slack] target={masked}")
    print("[verify-slack] sending synthetic advisory")

    payload = synthetic_payload()
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        args.webhook_url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "operator-wiring-verify/1.0",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=10.0) as resp:
            status = resp.status
            response_body = resp.read(500).decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        status = e.code
        response_body = e.read(500).decode("utf-8", errors="replace") if e.fp else ""
    except urllib.error.URLError as e:
        print(f"[verify-slack] FAIL — network error: {e.reason}", file=sys.stderr)
        return 3

    print(f"[verify-slack] HTTP {status}")
    print(f"[verify-slack] response body: {response_body.strip()[:200]}")
    if 200 <= status < 300 and response_body.strip().lower() == "ok":
        print("[verify-slack] PASS — posted to channel")
        print("[verify-slack] Manual: confirm message visible in the channel the webhook is bound to.")
        return 0

    print("[verify-slack] FAIL — Slack did not return 200/ok.", file=sys.stderr)
    if "invalid_token" in response_body or status == 404:
        print("[verify-slack] hint: webhook URL revoked or wrong. Re-create at api.slack.com/apps → Incoming Webhooks.", file=sys.stderr)
    elif "invalid_payload" in response_body or "invalid_blocks" in response_body:
        print("[verify-slack] hint: payload validation failed. Test in Block Kit Builder.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
