#!/usr/bin/env python3
"""config-validator.py — sanity-check an operator's wiring config files.

Validates:
  paging-config.json — pager + slack routing (required fields, URL shape, key non-default, threshold sane)
  otel-config.yaml   — OTEL exporter endpoint + headers (basic YAML-shape sniff; does not require PyYAML)

Usage:
  config-validator.py paging-config.json
  config-validator.py --all paging-config.json otel-config.yaml

Exit codes:
  0 = all configs valid
  1 = at least one config has FAIL-level errors
  2 = file missing / unreadable
"""

from __future__ import annotations

import argparse
import json
import socket
import sys
import urllib.parse
from pathlib import Path


DEFAULT_PLACEHOLDERS = {
    "",
    "CHANGE_ME",
    "REPLACE_ME",
    "your-key-here",
    "your-token-here",
    "xxx",
    "TODO",
    "<paste-here>",
}


def _dns_resolvable(host: str) -> tuple[bool, str]:
    try:
        socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
        return True, "dns ok"
    except socket.gaierror as e:
        return False, f"dns fail: {e}"


def _validate_url(label: str, url: str, require_https: bool = True) -> list[str]:
    out: list[str] = []
    if not url:
        out.append(f"{label}: empty URL")
        return out
    try:
        p = urllib.parse.urlparse(url)
    except Exception as e:  # noqa: BLE001
        out.append(f"{label}: cannot parse url ({e})")
        return out
    if p.scheme not in ("http", "https"):
        out.append(f"{label}: scheme={p.scheme!r}, expected http(s)")
    if require_https and p.scheme != "https":
        out.append(f"{label}: must be https in prod (got {p.scheme})")
    if not p.hostname:
        out.append(f"{label}: missing hostname")
    else:
        ok, msg = _dns_resolvable(p.hostname)
        if not ok:
            out.append(f"{label}: hostname={p.hostname} — {msg}")
    return out


def _is_default(val: str | None) -> bool:
    if val is None:
        return True
    return val.strip() in DEFAULT_PLACEHOLDERS


def validate_paging_config(path: Path) -> tuple[int, list[str]]:
    findings: list[str] = []
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return 2, [f"{path}: file not found"]
    except json.JSONDecodeError as e:
        return 1, [f"{path}: invalid JSON — {e}"]

    # required top-level keys
    for k in ("pager", "rate_limit"):
        if k not in doc:
            findings.append(f"missing top-level key: {k!r}")

    pager = doc.get("pager") or {}
    provider = pager.get("provider")
    if provider not in ("pagerduty", "opsgenie", "none"):
        findings.append(f"pager.provider must be 'pagerduty', 'opsgenie', or 'none' (got {provider!r})")

    if provider == "pagerduty":
        url = pager.get("events_url") or "https://events.pagerduty.com/v2/enqueue"
        findings += _validate_url("pager.events_url", url, require_https=True)
        key = pager.get("integration_key")
        if _is_default(key):
            findings.append("pager.integration_key is empty or a placeholder")

    elif provider == "opsgenie":
        url = pager.get("alerts_url") or "https://api.opsgenie.com/v2/alerts"
        findings += _validate_url("pager.alerts_url", url, require_https=True)
        key = pager.get("api_key")
        if _is_default(key):
            findings.append("pager.api_key is empty or a placeholder")
        if not pager.get("team"):
            findings.append("pager.team is empty (required for opsgenie routing)")

    slack = doc.get("slack") or {}
    if slack:
        url = slack.get("webhook_url")
        if _is_default(url):
            findings.append("slack.webhook_url is empty or a placeholder")
        else:
            findings += _validate_url("slack.webhook_url", url, require_https=True)
            if not url.startswith("https://hooks.slack.com/services/"):
                findings.append("slack.webhook_url does not look like a Slack incoming webhook")

    rl = doc.get("rate_limit") or {}
    max_pages = rl.get("max_pages_per_hour")
    if max_pages is None:
        findings.append("rate_limit.max_pages_per_hour missing")
    elif not isinstance(max_pages, (int, float)):
        findings.append(f"rate_limit.max_pages_per_hour must be number (got {type(max_pages).__name__})")
    elif max_pages < 1 or max_pages > 100:
        findings.append(f"rate_limit.max_pages_per_hour={max_pages} outside sane range (1..100)")

    has_fail = any(f for f in findings)
    return (1 if has_fail else 0), findings


def validate_otel_config(path: Path) -> tuple[int, list[str]]:
    findings: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return 2, [f"{path}: file not found"]

    # YAML-shape sniff without pulling in PyYAML — look for known keys at any depth
    needed = ("endpoint", "exporters", "service")
    for n in needed:
        if n not in text:
            findings.append(f"{path}: expected to see {n!r} somewhere (basic YAML sniff)")

    # extract endpoint values via simple line parse
    for ln in text.splitlines():
        s = ln.strip()
        if s.startswith("endpoint:"):
            val = s.split(":", 1)[1].strip().strip("'\"")
            if val and val not in ("0.0.0.0:4317", "0.0.0.0:4318", "127.0.0.1:4318"):
                findings += _validate_url(f"otel endpoint", val, require_https=False)

    return (1 if findings else 0), findings


def main() -> int:
    p = argparse.ArgumentParser(description="validate operator wiring config files")
    p.add_argument("paths", nargs="+", help="config file paths")
    p.add_argument("--all", action="store_true", help="validate every file (else stop on first FAIL)")
    args = p.parse_args()

    worst = 0
    for s in args.paths:
        path = Path(s)
        if path.name.endswith(".json"):
            code, findings = validate_paging_config(path)
        elif path.suffix in (".yaml", ".yml"):
            code, findings = validate_otel_config(path)
        else:
            print(f"[config-validator] {path}: unsupported file type — skipping", file=sys.stderr)
            continue

        if code == 0 and not findings:
            print(f"[config-validator] {path}: OK")
        else:
            label = "FAIL" if code == 1 else "MISSING"
            print(f"[config-validator] {path}: {label}", file=sys.stderr)
            for f in findings:
                print(f"  - {f}", file=sys.stderr)
            worst = max(worst, code)
            if not args.all and code != 0:
                return worst

    return worst


if __name__ == "__main__":
    sys.exit(main())
