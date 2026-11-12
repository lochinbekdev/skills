#!/usr/bin/env bash
# Bundle the canonical shared docs into each skill so skills are self-contained.
# Claude Code loads a skill by its own directory; a repo-root `docs/` path is not
# resolvable at runtime, so each skill references `references/<doc>.md` next to its
# SKILL.md. Run this after editing anything under docs/.
#
# Usage: scripts/sync-docs.sh
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DOCS_DIR="$REPO_ROOT/docs"
copied=0
for skill in "$REPO_ROOT"/skills/security/*/; do
  dest="$skill/references"
  mkdir -p "$dest"
  for doc in "$DOCS_DIR"/*.md; do
    cp "$doc" "$dest/"
    copied=$((copied + 1))
  done
done
echo "synced $copied doc copies into skill references/"
