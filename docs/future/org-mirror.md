# Layer 4: Org-Mirror Pattern-Precedent

This is a forward-looking record, **not a shipped layer**. The s2.0 lifecycle research recommendation honestly downgraded Layer 4 (optional org-mirror) to "pattern-precedent only" because no canonical cross-ecosystem spec exists. This doc captures the strongest analogue plus the trigger conditions for when to build.

## Strongest analogue: Cargo source-replacement

Cargo's `[source]` table in `.cargo/config.toml` lets a Cargo project resolve registry sources from an alternate location. Most production-grade analogue for "single internal mirror for all vis consumers" in our ecosystem.

> "Sources can be replaced with another source which acts as an overlay. The replacement source can be used as if it were the source being replaced."
> — `https://doc.rust-lang.org/cargo/reference/source-replacement.html`, official, 2024

```toml
[source.crates-io]
replace-with = "internal-mirror"

[source.internal-mirror]
registry = "https://internal-nexus.example.com/cargo"
```

The same shape for our ecosystem would be a `.vis-source` config (or env var) that overrides where `bootstrap.sh` clones `vis` from. Implementation precedent already exists in our bootstrap: `ENCHANTER_VIS_REPO` env var.

## Trigger conditions (build only when these fire)

Build the org-mirror layer **only** when at least one of:

1. **Air-gapped CI** — the CI environment cannot reach `github.com` and a sibling repo needs the conduct stack to run.
2. **SLA requiring github-uptime independence** — an enterprise customer demands the ecosystem keep working through a hypothetical github outage.
3. **Volunteer mirror owner** — someone in the ecosystem has signed up to host + maintain the mirror; without an owner, ship the layer and it bit-rots.

Below 1 of 3 is shipped: keep `bootstrap.sh`'s `ENCHANTER_VIS_REPO` env var (already in v0.6.0) as the escape hatch for ad-hoc operators who need it.

## Why not build it now

- Zero current consumers requesting it.
- The env-var escape hatch in `bootstrap.sh` covers 80% of the value at 1% of the cost.
- Building an unstaffed mirror introduces drift risk (mirror falls behind canonical, consumers get stale conduct).
- Cargo source-replacement docs say nothing about reconciliation when mirror diverges — that gap is the production cost of a real mirror.

## When triggers fire

Open a roadmap (Wixie convention: `state/roadmaps/<date>-org-mirror-build/`) and run the same research → craft → converge → harden → test lifecycle that produced this whole layer system. Don't bypass — the lifecycle worked end-to-end.
