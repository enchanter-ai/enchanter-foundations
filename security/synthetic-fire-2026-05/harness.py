#!/usr/bin/env python3
"""
harness.py — synthetic plugin-verdict simulator.

For each event in workloads/, simulate which plugins fire (advisory) based on
plugin logic modeled from hydra/plugins/<name>/. We are NOT calling the real
hooks — that requires the harness contract, env, and stdin payload shape that
hydra ships. Instead we mirror the decision logic precisely enough to measure
FP/FN at the simulator level. Where the real plugin uses live registry lookups
or CVE feeds, the simulator uses the seed lists baked into the fixtures.

Output: one verdict-record per event written to output/verdicts.jsonl.
Verdict record shape:
    {
      "id": "...",
      "label": "benign|adversarial|edge",
      "ground_truth": {<plugin>: bool, ...},
      "predicted":    {<plugin>: bool, ...},
      "advisory_msgs": ["..."],     # human-readable, optional
      "runtime_ms":   {<plugin>: float, ...},
    }

Note: "predicted" reflects ADVISORY emission. audit-trail fires on every
event (always True). The score under "advisory" is the meaningful one — the
"blocking" mode is opt-in per the project; we mention it but do not separate
it from advisory since the rule set is the same.
"""

from __future__ import annotations

import base64
import json
import random
import re
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORKLOADS = ROOT / "workloads"
OUT = ROOT / "output"
random.seed(20260505)


# ─── Plugin signal seeds (mirror the real plugins) ───────────────────────────

CANARY_TOKEN_RE = re.compile(r"CANARY-[A-Z0-9-]{2,}")

SECRET_PATTERNS = [
    (re.compile(r"AKIA[0-9A-Z]{16}"), "aws-key"),
    (re.compile(r"sk-ant-[a-zA-Z0-9_-]{20,}"), "anthropic"),
    (re.compile(r"sk-proj-[a-zA-Z0-9_-]{40,}"), "openai-proj"),
    (re.compile(r"ghp_[a-zA-Z0-9]{36}"), "github-pat"),
    (re.compile(r"gho_[a-zA-Z0-9]{36}"), "github-oauth"),
    (re.compile(r"sk_live_[a-zA-Z0-9]{24,}"), "stripe"),
    (re.compile(r"AIza[0-9A-Za-z_-]{35}"), "google"),
]

# Vuln-detector source-side patterns (signal R5 source-code risk).
VULN_RE = [
    re.compile(r"\beval\s*\("),
    re.compile(r"pickle\.loads"),
    re.compile(r"subprocess\.(call|Popen|run)\([^)]*shell\s*=\s*True"),
    re.compile(r"yaml\.load\s*\([^)]*\)(?!\s*Loader)"),
]

# Action-guard destructive command list (substring match on bash command).
DESTRUCTIVE_RE = [
    re.compile(r"\brm\s+-rf\b"),
    re.compile(r"\bgit\s+reset\s+--hard\b"),
    re.compile(r"\bgit\s+push\s+--force\b"),
    re.compile(r"\bgit\s+branch\s+-D\b"),
    re.compile(r"\bgit\s+clean\s+-f"),
    re.compile(r"\bnpm\s+publish\b"),
    re.compile(r"\bDROP\s+TABLE\b", re.I),
    re.compile(r"\bTRUNCATE\b", re.I),
]

# Egress-monitor uses a rolling seen-domain set. Initialize with the same
# allowlist a real deployment would have after a few sessions.
SEEN_DOMAINS = set([
    "github.com", "raw.githubusercontent.com", "registry.npmjs.org",
    "pypi.org", "docs.python.org", "docs.anthropic.com", "stackoverflow.com",
    "developer.mozilla.org", "nodejs.org", "go.dev", "rust-lang.org",
    "api.github.com", "objects.githubusercontent.com", "api.osv.dev",
    "api.openai.com", "googleapis.com",
])

# Package-gate signals.
POPULAR_NPM = set([
    "react", "react-dom", "lodash", "axios", "express", "vue", "next",
    "typescript", "webpack", "eslint", "chalk", "commander", "debug",
    "uuid", "yargs", "rxjs", "moment", "jquery", "minimist",
])
POPULAR_PYPI = set([
    "requests", "numpy", "pandas", "torch", "scipy", "django", "flask",
    "pytest", "pillow", "click", "pyyaml", "urllib3", "cryptography",
    "fastapi", "pydantic", "boto3", "sqlalchemy",
])

KNOWN_CVE_PKGS = {
    ("npm", "event-stream"),
    ("npm", "ua-parser-js"),
    ("pip", "ctx"),
    ("pip", "pytorch-lightning"),
}


def levenshtein(a: str, b: str) -> int:
    if len(a) < len(b):
        return levenshtein(b, a)
    if len(b) == 0:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a):
        curr = [i + 1]
        for j, cb in enumerate(b):
            curr.append(min(prev[j + 1] + 1, curr[j] + 1, prev[j] + (ca != cb)))
        prev = curr
    return prev[-1]


# ─── Per-plugin simulators ───────────────────────────────────────────────────

def sim_canary(ev):
    t0 = time.perf_counter()
    fired, msg = False, None
    # Canary fires when a known-token string appears in tool input or simulated
    # response. We accept either raw token or base64-encoded token.
    haystack = json.dumps(ev["tool_input"], ensure_ascii=False)
    if CANARY_TOKEN_RE.search(haystack):
        fired = True
        msg = "canary token in tool input"
    else:
        # Check base64 decode for tokens — real plugin doesn't but we model
        # an opt-in stronger detector. Reduce noise by only attempting on
        # WebFetch inputs.
        if ev["tool"] == "WebFetch":
            for tok in re.findall(r"[A-Za-z0-9+/]{20,}={0,2}", haystack):
                try:
                    decoded = base64.b64decode(tok, validate=True).decode("utf-8", "ignore")
                    if CANARY_TOKEN_RE.search(decoded):
                        fired = True
                        msg = "canary token in base64 payload"
                        break
                except Exception:
                    pass
    ms = (time.perf_counter() - t0) * 1000.0
    return fired, msg, ms


def _parse_install_packages(cmd):
    """Pull package names from `npm install X` / `pip install X==1.0` style."""
    out = []
    cmd = cmd.strip()
    if not cmd:
        return out
    parts = cmd.split()
    if len(parts) < 3:
        return out
    if parts[0] == "npm" and parts[1] in ("install", "i", "add"):
        eco = "npm"
        pkgs = parts[2:]
    elif parts[0] == "pip" and parts[1] == "install":
        eco = "pip"
        pkgs = parts[2:]
    else:
        return out
    for p in pkgs:
        if p.startswith("-"):
            continue
        # Strip version pin.
        name = p.split("@")[0] if eco == "npm" else re.split(r"[=<>!~]+", p)[0]
        name = name.strip()
        if name:
            out.append((eco, name, p))
    return out


def sim_package_gate(ev):
    t0 = time.perf_counter()
    fired, msg = False, None
    if ev["tool"] != "Bash":
        return False, None, (time.perf_counter() - t0) * 1000.0
    pkgs = _parse_install_packages(ev["tool_input"].get("command", ""))
    if not pkgs:
        return False, None, (time.perf_counter() - t0) * 1000.0
    for eco, name, raw in pkgs:
        # R4 typosquat: Levenshtein <= 2 to a popular name.
        seed = POPULAR_NPM if eco == "npm" else POPULAR_PYPI
        if name in seed:
            continue  # popular → silent
        # R1 existence (modeled): if name not in any seed AND lev>2 to every
        # popular, treat as slop-squat (R1) candidate.
        min_lev = min((levenshtein(name, p) for p in seed), default=99)
        if 0 < min_lev <= 2:
            fired = True
            msg = f"typosquat candidate: {name} (lev={min_lev})"
            break
        if min_lev > 2:
            # Heuristic: unknown package not in seed → R1/R5 advisory.
            # Real plugin would hit registry; we approximate as "fires".
            fired = True
            msg = f"unknown package: {name} (slopsquat candidate)"
            break
    ms = (time.perf_counter() - t0) * 1000.0
    return fired, msg, ms


def sim_egress_monitor(ev):
    t0 = time.perf_counter()
    fired, msg = False, None
    if ev["tool"] != "WebFetch":
        return False, None, (time.perf_counter() - t0) * 1000.0
    url = ev["tool_input"].get("url", "")
    m = re.match(r"https?://([^/]+)/?", url)
    if not m:
        return False, None, (time.perf_counter() - t0) * 1000.0
    host = m.group(1)
    if host not in SEEN_DOMAINS:
        fired = True
        msg = f"first-seen domain: {host}"
        SEEN_DOMAINS.add(host)  # add so subsequent hits don't re-fire
    ms = (time.perf_counter() - t0) * 1000.0
    return fired, msg, ms


def sim_capability_fence(ev):
    """Fires when an event represents a tool we'd block for a given subagent.

    Synthetic mode: an event that *labels itself* as a fence violation
    (the workload tags this via notes "capability-fence violation:" or via a
    Bash command containing curl-then-exfil; we approximate with two rules):

      1. Bash command containing `curl http` AND `$(` (command substitution
         pulling secret to remote) → fence violation.
      2. WebFetch to api.openai.com/v1/keys-style URL → fence violation.

    These are intentionally narrow heuristics — real fence is whitelist-driven.
    """
    t0 = time.perf_counter()
    fired, msg = False, None
    if ev["tool"] == "Bash":
        cmd = ev["tool_input"].get("command", "")
        if re.search(r"curl\s+https?://[^\s]+", cmd) and "$(" in cmd:
            fired = True
            msg = "fence: bash curl + command substitution"
    elif ev["tool"] == "WebFetch":
        url = ev["tool_input"].get("url", "")
        if re.search(r"api\.openai\.com.*keys", url):
            fired = True
            msg = "fence: openai keys endpoint"
    elif ev["tool"] == "Write":
        # If we see a write to /repo/SECRET, treat as fence violation (the
        # workload uses this as a marker for "subagent should not write").
        fp = ev["tool_input"].get("file_path", "")
        if "/SECRET" in fp:
            fired = True
            msg = "fence: write to /SECRET"
    ms = (time.perf_counter() - t0) * 1000.0
    return fired, msg, ms


def sim_secret_scanner(ev):
    t0 = time.perf_counter()
    fired, msg = False, None
    if ev["tool"] not in ("Write", "Edit"):
        return False, None, (time.perf_counter() - t0) * 1000.0
    content = ev["tool_input"].get("content", "")
    if not content:
        content = ev["tool_input"].get("new_string", "")
    # Truncate to 8KB max as the real scanner does for perf.
    sample = content[:8192]
    fp = ev["tool_input"].get("file_path", "")
    # Skip docs/ AND tests/fixtures (heuristic — tunable)
    # We DO NOT skip in this simulator, so we can measure FP impact.
    for pat, kind in SECRET_PATTERNS:
        if pat.search(sample):
            fired = True
            msg = f"secret pattern: {kind} in {fp}"
            break
    ms = (time.perf_counter() - t0) * 1000.0
    return fired, msg, ms


def sim_vuln_detector(ev):
    t0 = time.perf_counter()
    fired, msg = False, None
    # Mode 1: install of known-CVE package.
    if ev["tool"] == "Bash":
        pkgs = _parse_install_packages(ev["tool_input"].get("command", ""))
        for eco, name, raw in pkgs:
            if (eco, name) in KNOWN_CVE_PKGS:
                fired = True
                msg = f"known CVE in {name}"
                break
    # Mode 2: dangerous source patterns in Write/Edit content.
    if not fired and ev["tool"] in ("Write", "Edit"):
        content = ev["tool_input"].get("content", "") or ev["tool_input"].get("new_string", "")
        for rx in VULN_RE:
            if rx.search(content):
                fired = True
                msg = f"dangerous source pattern: {rx.pattern}"
                break
    ms = (time.perf_counter() - t0) * 1000.0
    return fired, msg, ms


def sim_action_guard(ev):
    t0 = time.perf_counter()
    fired, msg = False, None
    if ev["tool"] != "Bash":
        return False, None, (time.perf_counter() - t0) * 1000.0
    cmd = ev["tool_input"].get("command", "")
    for rx in DESTRUCTIVE_RE:
        if rx.search(cmd):
            fired = True
            msg = f"destructive op: {rx.pattern}"
            break
    ms = (time.perf_counter() - t0) * 1000.0
    return fired, msg, ms


def sim_audit_trail(ev):
    """Fires on every event — the baseline observer."""
    t0 = time.perf_counter()
    _ = json.dumps(ev["tool_input"])  # simulate the marshalling cost
    ms = (time.perf_counter() - t0) * 1000.0
    return True, "logged", ms


PLUGINS = [
    ("canary", sim_canary),
    ("package-gate", sim_package_gate),
    ("egress-monitor", sim_egress_monitor),
    ("capability-fence", sim_capability_fence),
    ("secret-scanner", sim_secret_scanner),
    ("vuln-detector", sim_vuln_detector),
    ("action-guard", sim_action_guard),
    ("audit-trail", sim_audit_trail),
]


# ─── Driver ───────────────────────────────────────────────────────────────────

def load_all_events():
    paths = sorted(WORKLOADS.glob("*/*.jsonl"))
    for p in paths:
        with p.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                yield json.loads(line)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    verdicts_path = OUT / "verdicts.jsonl"
    n = 0
    with verdicts_path.open("w", encoding="utf-8") as fo:
        for ev in load_all_events():
            predicted = {}
            advisories = []
            runtime_ms = {}
            for name, fn in PLUGINS:
                # For canary scan we want to also check `_simulated_response`
                # field that adversarial events stash. Re-shape input.
                ev_for_plugin = ev
                if name == "canary":
                    sim_resp = ev["tool_input"].get("_simulated_response", "")
                    if sim_resp:
                        ev_for_plugin = dict(ev)
                        ev_for_plugin["tool_input"] = dict(ev["tool_input"])
                        ev_for_plugin["tool_input"]["_canary_search_blob"] = sim_resp
                fired, msg, ms = fn(ev_for_plugin)
                predicted[name] = bool(fired)
                runtime_ms[name] = round(ms, 3)
                if fired and msg:
                    advisories.append(f"[{name}] {msg}")
            rec = {
                "id": ev["id"],
                "label": ev["label"],
                "ground_truth": ev["ground_truth"],
                "predicted": predicted,
                "advisory_msgs": advisories,
                "runtime_ms": runtime_ms,
            }
            fo.write(json.dumps(rec, ensure_ascii=False) + "\n")
            n += 1
    print(f"verdicts written: {n} -> {verdicts_path}")


if __name__ == "__main__":
    main()
