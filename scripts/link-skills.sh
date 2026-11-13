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
pruned=0
for target in "${TARGETS[@]}"; do
  mkdir -p "$target"
  # Drop links this script created earlier that now dangle, e.g. after a skill
  # is renamed or removed upstream. Only symlinks into this repo are touched.
  for link in "$target"/*; do
    [ -L "$link" ] || continue
    dest="$(readlink "$link")"
    case "$dest" in
      "$SKILLS_DIR"/*)
        if [ ! -d "$dest" ]; then
          rm -f "$link"
          echo "pruned  $link (dangling -> $dest)"
          pruned=$((pruned + 1))
        fi
        ;;
    esac
  done
  for skill in "$SKILLS_DIR"/*/; do
    name="$(basename "$skill")"
    link="$target/$name"
    rm -rf "$link"
    ln -s "${skill%/}" "$link"
    echo "linked  $link -> ${skill%/}"
    linked=$((linked + 1))
  done
done

echo "done: $linked symlink(s) created, $pruned pruned"
