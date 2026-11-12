#!/usr/bin/env bash
# Link every skill into the local agent skill directories so non-Claude-Code
# agents (e.g. OpenAI Codex) discover them. Each link points back into this
# repo, so a `git pull` keeps the installed skills current.
#
# Usage: scripts/link-skills.sh
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_DIR="$REPO_ROOT/skills/security"

# Target harness skill directories. Add/remove as your agents require.
TARGETS=(
  "$HOME/.agents/skills"   # OpenAI Codex / generic agents
  "$HOME/.claude/skills"   # Claude Code (local, outside the plugin)
)

linked=0
for target in "${TARGETS[@]}"; do
  mkdir -p "$target"
  for skill in "$SKILLS_DIR"/*/; do
    name="$(basename "$skill")"
    link="$target/$name"
    rm -rf "$link"
    ln -s "${skill%/}" "$link"
    echo "linked  $link -> ${skill%/}"
    linked=$((linked + 1))
  done
done

echo "done: $linked symlink(s) created"
