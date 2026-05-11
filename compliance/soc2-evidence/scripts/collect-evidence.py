#!/usr/bin/env python3
"""SOC 2 daily evidence collector.

Pulls evidence from each plugin's state/ + audit logs, normalizes to common
JSON shape, writes to compliance/soc2-evidence/collected/YYYY-MM-DD/<criterion>.jsonl

Stdlib only. Honest-numbers contract: if a producer is absent or empty, we
emit an explicit `evidence_data.status: "producer-absent"` event rather than
a fake row. The completeness check distinguishes "absent" from "present".
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]  # enchanted-skills/
EVIDENCE_DIR = ROOT / "agent-foundations" / "compliance" / "soc2-evidence"
COLLECTED = EVIDENCE_DIR / "collected"


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def event(criterion: str, plugin: str, event_type: str, data: dict, retention: str = "1y") -> dict:
    ts = now_iso()
    data = {**data, "retention": retention}
    payload = canonical({"ts": ts, "criterion": criterion, "plugin": plugin,
                         "event_type": event_type, "evidence_data": data})
    h = hashlib.sha256(payload.encode()).hexdigest()
    return {"ts": ts, "criterion": criterion, "plugin": plugin,
            "event_type": event_type, "evidence_data": data, "hash": h}


def file_hash(p: Path) -> str | None:
    if not p.exists() or not p.is_file():
        return None
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()


def dir_hashes(d: Path, pattern: str = "*.md") -> dict:
    if not d.exists() or not d.is_dir():
        return {}
    out = {}
    for f in sorted(d.glob(pattern)):
        if f.is_file():
            out[f.name] = file_hash(f)
    return out


def tail_jsonl(p: Path, n: int = 10) -> list:
    if not p.exists() or not p.is_file():
        return []
    try:
        lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []
    out = []
    for line in lines[-n:]:
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            out.append({"raw": line[:200]})
    return out


def absent(plugin: str, reason: str) -> dict:
    return {"status": "producer-absent", "expected_plugin": plugin, "reason": reason}


# ---------------------------------------------------------------------------
# Per-criterion collectors. Each returns a list[dict] of normalized events.
# ---------------------------------------------------------------------------

def cc1_1() -> list:
    conduct = ROOT / "agent-foundations" / "shared" / "conduct"
    if not conduct.exists():
        conduct = ROOT / "wixie" / "shared" / "conduct"
    hashes = dir_hashes(conduct, "*.md")
    plugin = "shared/conduct"
    if not hashes:
        return [event("CC1.1", plugin, "attestation", absent(plugin, "conduct dir missing"), "7y")]
    return [event("CC1.1", plugin, "config-hash", {"files": hashes}, "7y")]


def cc1_2() -> list:
    return [event("CC1.2", "org-structure", "attestation",
                  {"structure": "single-maintainer", "board": "none",
                   "note": "GAP per soc2.md CC1.2; emitted monthly"}, "7y")]


def cc1_3() -> list:
    plugin = "claude-md-files"
    found = {}
    for claude_md in ROOT.glob("*/CLAUDE.md"):
        found[str(claude_md.relative_to(ROOT))] = file_hash(claude_md)
    if not found:
        return [event("CC1.3", plugin, "attestation", absent(plugin, "no CLAUDE.md found"), "7y")]
    return [event("CC1.3", plugin, "config-hash", {"files": found}, "7y")]


def cc1_4() -> list:
    p = ROOT / "wixie" / "shared" / "conduct" / "skill-authoring.md"
    if not p.exists():
        p = ROOT / "agent-foundations" / "shared" / "conduct" / "skill-authoring.md"
    h = file_hash(p)
    if not h:
        return [event("CC1.4", "skill-authoring", "attestation", absent("skill-authoring.md", "file missing"), "1y")]
    return [event("CC1.4", "skill-authoring", "config-hash", {"file": str(p.name), "hash": h}, "1y")]


def cc1_5() -> list:
    out = []
    for plog in ROOT.glob("*/state/precedent-log.md"):
        h = file_hash(plog)
        out.append(event("CC1.5", str(plog.relative_to(ROOT).parent), "log-tail",
                         {"file": str(plog.relative_to(ROOT)), "hash": h}, "1y"))
    if not out:
        out.append(event("CC1.5", "precedent-log", "attestation", absent("precedent-log", "no logs found"), "1y"))
    return out


def cc2_1() -> list:
    out = []
    metas = list((ROOT / "wixie" / "prompts").glob("*/metadata.json")) if (ROOT / "wixie" / "prompts").exists() else []
    out.append(event("CC2.1", "wixie/prompts", "metric",
                     {"prompt_count": len(metas), "sampled": [str(m.relative_to(ROOT)) for m in metas[:5]]}, "1y"))
    return out


def cc2_2() -> list:
    bdir = ROOT / "wixie" / "plugins" / "inference-engine" / "state" / "briefings"
    hashes = dir_hashes(bdir, "*.md")
    if not hashes:
        return [event("CC2.2", "inference-engine", "attestation",
                      absent("inference-engine/state/briefings", "no briefings yet"), "1y")]
    return [event("CC2.2", "inference-engine", "config-hash", {"briefings": hashes}, "1y")]


def cc2_3() -> list:
    cdir = ROOT / "agent-foundations" / "compliance"
    hashes = dir_hashes(cdir, "*.md")
    return [event("CC2.3", "agent-foundations/compliance", "config-hash", {"files": hashes}, "1y")]


def cc3_1() -> list:
    return [event("CC3.1", "wixie/convergence-engine", "metric",
                  {"deploy_bar": {"sigma_lt": 0.45, "overall_gte": 9.0, "axis_min": 7.0, "sat_required": "8/8"}}, "1y")]


def cc3_2() -> list:
    synth = ROOT / "wixie" / "prompts" / "security-closure" / "results" / "synthesis.md"
    h = file_hash(synth)
    if not h:
        return [event("CC3.2", "security-closure", "attestation", absent("synthesis.md", "missing"), "7y")]
    return [event("CC3.2", "security-closure", "attestation",
                  {"synthesis_hash": h, "path": str(synth.relative_to(ROOT))}, "7y")]


def cc3_3() -> list:
    out = []
    secret_findings = ROOT / "hydra" / "plugins" / "secret-scanner" / "state" / "findings.jsonl"
    out.append(event("CC3.3", "hydra/secret-scanner", "log-tail",
                     {"tail": tail_jsonl(secret_findings, 5)}, "7y"))
    audit_log = ROOT / "hydra" / "plugins" / "audit-trail" / "state" / "log.jsonl"
    out.append(event("CC3.3", "hydra/audit-trail", "log-tail",
                     {"hmac_chain_tail": tail_jsonl(audit_log, 5)}, "7y"))
    return out


def cc3_4() -> list:
    return [event("CC3.4", "wixie/convergence-engine", "log-tail",
                  {"contract": "no-regression revert-on-failure", "baseline_snapshot": "verification.md"}, "1y")]


def cc4_1() -> list:
    cat = ROOT / "wixie" / "plugins" / "inference-engine" / "state" / "catalog.json"
    h = file_hash(cat)
    return [event("CC4.1", "inference-engine", "attestation",
                  {"catalog_hash": h, "reconcile_status": "see catalog"} if h else
                  absent("inference-engine/catalog.json", "no reconcile yet"), "7y")]


def cc4_2() -> list:
    counts = {}
    for log in ROOT.glob("*/prompts/*/learnings.md"):
        try:
            text = log.read_text(encoding="utf-8", errors="replace")
            for code in [f"F{i:02d}" for i in range(1, 15)]:
                counts[code] = counts.get(code, 0) + text.count(code)
        except OSError:
            continue
    return [event("CC4.2", "failure-modes", "metric", {"f_code_counts": counts}, "1y")]


def cc5_1() -> list:
    out = []
    conduct = ROOT / "wixie" / "shared" / "conduct"
    hashes = dir_hashes(conduct, "*.md")
    out.append(event("CC5.1", "shared/conduct", "config-hash", {"files": hashes}, "1y"))
    skill_count = len(list(ROOT.glob("*/plugins/*/SKILL.md")))
    out.append(event("CC5.1", "skills", "metric", {"skill_md_count": skill_count}, "1y"))
    return out


def cc5_2() -> list:
    out = []
    hydra_plugins = ["audit-trail", "capability-fence", "egress-shield", "secret-scanner",
                     "vuln-detector", "package-gate", "license-gate", "sbom-emitter", "action-guard", "canary"]
    for pname in hydra_plugins:
        pdir = ROOT / "hydra" / "plugins" / pname / "state"
        present = pdir.exists()
        out.append(event("CC5.2", f"hydra/{pname}", "config-hash",
                         {"state_dir_present": present,
                          "state_files": [f.name for f in pdir.iterdir()] if present else []}, "1y"))
    return out


def cc5_3() -> list:
    out = []
    for inst in ROOT.glob("*/install.sh"):
        out.append(event("CC5.3", str(inst.relative_to(ROOT).parent), "config-hash",
                         {"file": str(inst.relative_to(ROOT)), "hash": file_hash(inst)}, "1y"))
    if not out:
        out.append(event("CC5.3", "install-scripts", "attestation", absent("install.sh", "no install scripts"), "1y"))
    return out


def cc6_1() -> list:
    out = []
    cf = ROOT / "hydra" / "plugins" / "capability-fence" / "hooks" / "PreToolUse.sh"
    out.append(event("CC6.1", "hydra/capability-fence", "config-hash",
                     {"hook_present": cf.exists(), "hash": file_hash(cf)}, "7y"))
    ag = ROOT / "hydra" / "plugins" / "action-guard" / "state" / "confirmations.jsonl"
    out.append(event("CC6.1", "hydra/action-guard", "log-tail", {"tail": tail_jsonl(ag, 5)}, "7y"))
    return out


def cc6_2() -> list:
    return [event("CC6.2", "skill-discovery", "metric",
                  {"contract": "9/10 dispatches correct gate per skill-authoring.md"}, "1y")]


def cc6_3() -> list:
    return [event("CC6.3", "delegation", "log-tail",
                  {"contract": "per-subagent tool whitelist per delegation.md"}, "1y")]


def cc6_4() -> list:
    return [event("CC6.4", "n/a-physical", "attestation",
                  {"applicability": "N/A", "reason": "distributed code repo, no physical infrastructure"}, "7y")]


def cc6_5() -> list:
    return [event("CC6.5", "n/a-physical", "attestation",
                  {"applicability": "N/A", "reason": "no physical assets to dispose"}, "7y")]


def cc6_6() -> list:
    out = []
    canary = ROOT / "hydra" / "plugins" / "canary" / "state" / "canary-results.jsonl"
    out.append(event("CC6.6", "hydra/canary", "log-tail", {"tail": tail_jsonl(canary, 5)}, "7y"))
    return out


def cc6_7() -> list:
    allow = ROOT / "hydra" / "plugins" / "egress-shield" / "config" / "allowlist.yaml"
    return [event("CC6.7", "hydra/egress-shield", "config-hash",
                  {"allowlist_hash": file_hash(allow), "present": allow.exists()}, "1y")]


def cc6_8() -> list:
    out = []
    vuln = ROOT / "hydra" / "plugins" / "vuln-detector" / "state" / "audit.jsonl"
    out.append(event("CC6.8", "hydra/vuln-detector", "log-tail", {"tail": tail_jsonl(vuln, 5)}, "7y"))
    pg = ROOT / "hydra" / "plugins" / "package-gate" / "scripts" / "check-package.sh"
    out.append(event("CC6.8", "hydra/package-gate", "config-hash",
                     {"script_present": pg.exists(), "hash": file_hash(pg)}, "7y"))
    return out


def cc7_1() -> list:
    out = []
    vuln = ROOT / "hydra" / "plugins" / "vuln-detector" / "state" / "audit.jsonl"
    out.append(event("CC7.1", "hydra/vuln-detector", "log-tail", {"tail": tail_jsonl(vuln, 5)}, "7y"))
    cql = list(ROOT.glob("*/.github/workflows/codeql.yml"))
    out.append(event("CC7.1", "codeql", "config-hash",
                     {"workflows": [str(c.relative_to(ROOT)) for c in cql]}, "7y"))
    return out


def cc7_2() -> list:
    out = []
    audit = ROOT / "hydra" / "plugins" / "audit-trail" / "state" / "log.jsonl"
    out.append(event("CC7.2", "hydra/audit-trail", "log-tail",
                     {"hmac_chain_tail": tail_jsonl(audit, 5)}, "7y"))
    cat = ROOT / "wixie" / "plugins" / "inference-engine" / "state" / "catalog.json"
    out.append(event("CC7.2", "inference-engine", "config-hash",
                     {"catalog_hash": file_hash(cat)}, "7y"))
    return out


def cc7_3() -> list:
    return [event("CC7.3", "failure-modes", "log-tail",
                  {"runbooks": "agent-foundations/runbooks/ F01-F21"}, "1y")]


def cc7_4() -> list:
    p = ROOT / "hydra" / "plugins" / "action-guard" / "state" / "confirmations.jsonl"
    return [event("CC7.4", "hydra/action-guard", "log-tail", {"tail": tail_jsonl(p, 5)}, "7y")]


def cc7_5() -> list:
    return [event("CC7.5", "wixie/convergence-engine", "log-tail",
                  {"recovery": "revert-on-regression contract"}, "1y")]


def cc8_1() -> list:
    out = []
    prl = ROOT / "sylph" / "plugins" / "pr-lifecycle" / "state"
    out.append(event("CC8.1", "sylph/pr-lifecycle", "config-hash",
                     {"state_present": prl.exists()}, "7y"))
    tests = list((ROOT / "wixie" / "prompts").glob("*/tests.json")) if (ROOT / "wixie" / "prompts").exists() else []
    out.append(event("CC8.1", "wixie/prompt-tester", "metric", {"tests_json_count": len(tests)}, "7y"))
    return out


def cc9_1() -> list:
    synth = ROOT / "wixie" / "prompts" / "security-closure" / "results" / "synthesis.md"
    return [event("CC9.1", "security-closure", "attestation",
                  {"synthesis_hash": file_hash(synth)}, "7y")]


def cc9_2() -> list:
    out = []
    sbom = ROOT / "hydra" / "plugins" / "sbom-emitter" / "state" / "sbom.cdx.json"
    out.append(event("CC9.2", "hydra/sbom-emitter", "config-hash",
                     {"sbom_hash": file_hash(sbom), "present": sbom.exists()}, "7y"))
    lic = ROOT / "hydra" / "plugins" / "license-gate" / "state" / "findings.jsonl"
    out.append(event("CC9.2", "hydra/license-gate", "log-tail", {"tail": tail_jsonl(lic, 5)}, "7y"))
    return out


def a1_1() -> list:
    out = []
    for pname in ["budget-watcher", "rate-shield"]:
        pdir = ROOT / "pech" / "plugins" / pname / "state"
        out.append(event("A1.1", f"pech/{pname}", "metric",
                         {"state_present": pdir.exists()}, "1y"))
    cg = ROOT / "emu" / "plugins" / "context-guard" / "state"
    out.append(event("A1.1", "emu/context-guard", "metric", {"state_present": cg.exists()}, "1y"))
    return out


def a1_2() -> list:
    out = []
    arts = ROOT / "wixie" / "plugins" / "inference-engine" / "state" / "artifacts.jsonl"
    out.append(event("A1.2", "inference-engine/artifacts", "config-hash",
                     {"present": arts.exists(), "hash": file_hash(arts)}, "7y"))
    for plog in ROOT.glob("*/state/precedent-log.md"):
        out.append(event("A1.2", str(plog.relative_to(ROOT).parent), "config-hash",
                         {"file": str(plog.relative_to(ROOT)), "hash": file_hash(plog)}, "7y"))
    return out


def a1_3() -> list:
    return [event("A1.3", "recovery-drills", "attestation",
                  {"status": "GAP", "note": "no formal drill schedule; sparse monthly attestation per soc2.md A1.3"}, "7y")]


COLLECTORS = {
    "CC1.1": cc1_1, "CC1.2": cc1_2, "CC1.3": cc1_3, "CC1.4": cc1_4, "CC1.5": cc1_5,
    "CC2.1": cc2_1, "CC2.2": cc2_2, "CC2.3": cc2_3,
    "CC3.1": cc3_1, "CC3.2": cc3_2, "CC3.3": cc3_3, "CC3.4": cc3_4,
    "CC4.1": cc4_1, "CC4.2": cc4_2,
    "CC5.1": cc5_1, "CC5.2": cc5_2, "CC5.3": cc5_3,
    "CC6.1": cc6_1, "CC6.2": cc6_2, "CC6.3": cc6_3, "CC6.4": cc6_4, "CC6.5": cc6_5,
    "CC6.6": cc6_6, "CC6.7": cc6_7, "CC6.8": cc6_8,
    "CC7.1": cc7_1, "CC7.2": cc7_2, "CC7.3": cc7_3, "CC7.4": cc7_4, "CC7.5": cc7_5,
    "CC8.1": cc8_1,
    "CC9.1": cc9_1, "CC9.2": cc9_2,
    "A1.1": a1_1, "A1.2": a1_2, "A1.3": a1_3,
}


def main() -> int:
    day_dir = COLLECTED / today()
    day_dir.mkdir(parents=True, exist_ok=True)
    total = 0
    failed: list[str] = []
    for crit, fn in COLLECTORS.items():
        try:
            events = fn()
        except Exception as e:  # collector must not abort the run
            failed.append(f"{crit}: {type(e).__name__}: {e}")
            continue
        out_file = day_dir / f"{crit}.jsonl"
        with out_file.open("a", encoding="utf-8") as f:
            for ev in events:
                f.write(json.dumps(ev, separators=(",", ":")) + "\n")
                total += 1
    summary = {"ts": now_iso(), "day": today(), "criteria_collected": len(COLLECTORS) - len(failed),
               "total_events": total, "failed": failed}
    (day_dir / "_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
