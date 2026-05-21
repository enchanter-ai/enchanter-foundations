#!/bin/sh
# vis installer
#
# One-liner (vendored install at ./shared/vis):
#   curl -fsSL https://raw.githubusercontent.com/enchanter-ai/vis/main/install.sh | sh
#
# With options:
#   curl -fsSL https://raw.githubusercontent.com/enchanter-ai/vis/main/install.sh | sh -s -- --mode starter
#   ./install.sh --target vendor/vis --mode minimal
#   ./install.sh --submodule

set -eu

REPO_URL="https://github.com/enchanter-ai/vis.git"
TARGET="shared/vis"
MODE="full"
SUBMODULE=0

usage() {
  cat <<'EOF'
vis installer

Usage:
  install.sh [--target DIR] [--mode MODE] [--submodule]

Options:
  --target DIR    Where to install. Default: shared/vis
  --mode MODE     Which packages to keep (vis is a packages-monorepo; modes trim packages/):
                    full     every package + docs + roadmap-2026 (default)
                    starter  packages/{core,skills,web} + docs — production starter pack:
                             baseline conduct + F01-F14 + host recipes + web-fetch discipline
                    minimal  packages/core only — baseline conduct, F01-F14 taxonomy + runbooks,
                             glossary, anti-patterns, conduct-abi-check.sh
  --submodule     Install as a git submodule (history preserved, pinned via parent repo).
                  Default is a vendored copy with .git stripped — easier to drop into any project.
  -h, --help      Show this message and exit.

Examples:
  install.sh
  install.sh --mode starter
  install.sh --target vendor/vis --mode minimal
  install.sh --submodule
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    --target)    TARGET="${2:?--target requires a value}"; shift 2 ;;
    --mode)      MODE="${2:?--mode requires a value}"; shift 2 ;;
    --submodule) SUBMODULE=1; shift ;;
    -h|--help)   usage; exit 0 ;;
    *)           printf 'Unknown option: %s\n\n' "$1" >&2; usage >&2; exit 1 ;;
  esac
done

case "$MODE" in
  full|starter|minimal) ;;
  *) printf 'Invalid --mode: %s (expected: full | starter | minimal)\n' "$MODE" >&2; exit 1 ;;
esac

if ! command -v git >/dev/null 2>&1; then
  printf 'git is required but not installed.\n' >&2
  exit 1
fi

if [ -e "$TARGET" ]; then
  printf 'Target already exists: %s\nRemove it or pass a different --target.\n' "$TARGET" >&2
  exit 1
fi

PARENT_DIR=$(dirname -- "$TARGET")
[ -n "$PARENT_DIR" ] && mkdir -p -- "$PARENT_DIR"

if [ "$SUBMODULE" -eq 1 ]; then
  if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    printf '%s\n' '--submodule requires running inside a git repo.' >&2
    exit 1
  fi
  printf 'Adding submodule at %s ...\n' "$TARGET"
  git submodule add "$REPO_URL" "$TARGET" >/dev/null
else
  printf 'Cloning into %s ...\n' "$TARGET"
  git clone --depth 1 --quiet "$REPO_URL" "$TARGET"
  rm -rf -- "$TARGET/.git"
fi

# Trim per mode. vis is a packages-monorepo; modes drop whole packages from packages/.
# Top-level docs/, roadmap-2026/, package.json, install.sh, LICENSE, CHANGELOG.md are kept
# in full and starter; minimal drops top-level docs/ and roadmap-2026/ as well.
case "$MODE" in
  starter)
    # Keep: packages/{core,skills,web} + docs/. Drop everything else.
    rm -rf -- \
      "$TARGET/packages/orchestration" \
      "$TARGET/packages/safety" \
      "$TARGET/packages/memory" \
      "$TARGET/packages/cost" \
      "$TARGET/roadmap-2026"
    ;;
  minimal)
    # Keep packages/core only. Drop all sibling packages + cross-cutting docs.
    rm -rf -- \
      "$TARGET/packages/skills" \
      "$TARGET/packages/orchestration" \
      "$TARGET/packages/safety" \
      "$TARGET/packages/web" \
      "$TARGET/packages/memory" \
      "$TARGET/packages/cost" \
      "$TARGET/docs" \
      "$TARGET/roadmap-2026"
    ;;
esac

# Compute install kind for the success line
KIND="vendored"
[ "$SUBMODULE" -eq 1 ] && KIND="submodule"

cat <<EOF

Installed vis at $TARGET (mode: $MODE, $KIND).

Next steps:
  1. Reference modules from your CLAUDE.md, system prompt, or .cursor/rules:
       @$TARGET/packages/core/conduct/discipline.md
       @$TARGET/packages/core/conduct/verification.md
       @$TARGET/packages/core/conduct/tool-use.md

  2. Pick a recipe for your host:
       https://github.com/enchanter-ai/vis/tree/main/packages/skills/recipes
EOF
