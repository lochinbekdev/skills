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

# Only the cross-cutting standards every skill must follow are bundled. Repo-facing
# docs (e.g. harness-notes.md) stay under docs/ and out of the skills' context.
SHARED_DOCS=(
  intake.md
  write-boundary.md
  test-accounts.md
  report-standard.md
  tooling.md
  findings-quality.md
)

copied=0
for skill in "$REPO_ROOT"/skills/security/*/; do
  dest="$skill/references"
  mkdir -p "$dest"
  for doc in "${SHARED_DOCS[@]}"; do
    cp "$DOCS_DIR/$doc" "$dest/"
    copied=$((copied + 1))
  done
done
echo "synced $copied doc copies into skill references/"
