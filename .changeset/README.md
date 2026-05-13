# Changesets

Semver-aware change tracking for the enchanter-ai monorepo. Each material change to a versioned package ships with a *changeset* — a small markdown file declaring which packages bumped and why. CI consumes the accumulated changesets, opens a Versions PR, and (once merged) publishes the new versions.

## What changesets do

- **Track intent, not just diff.** A patch bump and a breaking change both touch lines; only a changeset distinguishes them.
- **Aggregate across PRs.** Multiple PRs land before a release; their changesets fold into one Versions PR.
- **Drive the changelog.** Each changeset becomes a row in `CHANGELOG.md` for its package, with a backlink to the originating PR.

## Create a changeset

Pre-req (one-time): `npm install` at the repo root installs the `@changesets/cli` dev dep.

```bash
pnpm changeset    # interactive: pick package(s), pick bump (patch/minor/major), write summary
git add .changeset/<generated>.md
git commit -m "chore(changeset): <one-line summary>"
```

The generated `.md` file lives alongside the change — same PR, same review.

If you don't have pnpm, `npx changeset` works after `npm install`.

## How CI consumes them

`.github/workflows/changesets.yml` runs on every push to `main`:

1. If pending changeset files exist → opens (or updates) a `chore: version packages` PR.
2. The Versions PR shows the proposed `package.json` bumps and `CHANGELOG.md` entries.
3. Merging the Versions PR triggers `npm run release` → publishes to npm (when `NPM_TOKEN` is set).

The author of a normal PR writes the changeset; the maintainer just merges the Versions PR.

## When to use

- **Conduct module changes** (`shared/conduct/*.md`) — these are the load-bearing artifact this repo exists to ship. Every meaningful edit gets a changeset.
- **Engine, recipe, runbook, or taxonomy changes** that downstream plugins consume.
- **Anything cross-repo** — if the change is meant to propagate to other enchanter-ai repos via the conduct-abi.yml pipeline (F-026), it must be versioned.

Skip changesets for: typo fixes in untracked docs, internal scaffolding, CI-only tweaks, README polish.

## Cross-repo strategy

Each enchanter-ai repo versions independently for now. `vis` is the canonical home for shared conduct; downstream plugin repos (wixie, hydra, sylph, …) consume conduct via the conduct-abi.yml propagation, not via npm dependency.

Future: once conduct ships as `@enchanter-ai/conduct` on npm, downstream repos will pin against published versions and changesets here will drive their dependency bumps directly. See `docs/CROSS_REPO_VERSIONING.md`.
