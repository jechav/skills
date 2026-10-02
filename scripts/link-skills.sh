#!/usr/bin/env bash
set -euo pipefail

# Dev-only: symlink every skill in this repo into the local skill directories
#   - ~/.claude/skills: Claude Code
#   - ~/.agents/skills: Codex and other Agent Skills-compatible tools
# Edits in the repo are picked up immediately. Re-run after adding, removing
# or renaming a skill.

REPO="$(cd "$(dirname "$0")/.." && pwd)"
DESTS=("$HOME/.claude/skills" "$HOME/.agents/skills")

for DEST in "${DESTS[@]}"; do
  mkdir -p "$DEST"
  while IFS= read -r -d '' skill_md; do
    src="$(dirname "$skill_md")"
    name="$(basename "$src")"
    target="$DEST/$name"
    if [ -e "$target" ] && [ ! -L "$target" ]; then
      echo "skip $target (exists and is not a symlink)" >&2
      continue
    fi
    ln -sfn "$src" "$target"
    echo "linked $name -> $DEST"
  done < <(find "$REPO/skills" -name SKILL.md -print0)
done
