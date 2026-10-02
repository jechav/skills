#!/usr/bin/env bash
set -euo pipefail

# Scaffold a new skill from templates/skill and register it everywhere it must
# be listed: .claude-plugin/plugin.json and the bucket README.
#
# Usage: scripts/new-skill.sh <bucket> <skill-name>
#   e.g. scripts/new-skill.sh productivity meeting-notes

if [ $# -ne 2 ]; then
  echo "usage: $0 <bucket> <skill-name>" >&2
  exit 1
fi

BUCKET="$1"
NAME="$2"
REPO="$(cd "$(dirname "$0")/.." && pwd)"
DIR="$REPO/skills/$BUCKET/$NAME"
PLUGIN="$REPO/.claude-plugin/plugin.json"

if ! [[ "$NAME" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]] || [ ${#NAME} -gt 64 ]; then
  echo "error: skill name must be lowercase letters, digits and hyphens (max 64 chars)" >&2
  exit 1
fi
if [ -e "$DIR" ]; then
  echo "error: $DIR already exists" >&2
  exit 1
fi

# "meeting-notes" -> "Meeting Notes"
TITLE="$(echo "$NAME" | awk -F- '{for (i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2)} 1' OFS=' ')"

mkdir -p "$DIR"
cp -R "$REPO/templates/skill/." "$DIR/"
for f in "$DIR/SKILL.md" "$DIR/agents/openai.yaml"; do
  sed -e "s/__NAME__/$NAME/g" -e "s/__TITLE__/$TITLE/g" "$f" > "$f.tmp" && mv "$f.tmp" "$f"
done

# Register in the Claude Code plugin manifest (kept sorted).
tmp="$(mktemp)"
jq --arg p "./skills/$BUCKET/$NAME" '.skills = ((.skills + [$p]) | unique)' "$PLUGIN" > "$tmp"
mv "$tmp" "$PLUGIN"

# Add to the bucket README, creating it if this is a new bucket.
README="$REPO/skills/$BUCKET/README.md"
if [ ! -f "$README" ]; then
  BUCKET_TITLE="$(echo "$BUCKET" | awk '{print toupper(substr($0,1,1)) substr($0,2)}')"
  printf '# %s\n\n' "$BUCKET_TITLE" > "$README"
fi
echo "- **[$NAME](./$NAME/SKILL.md)**: TODO one-line description." >> "$README"

echo "created skills/$BUCKET/$NAME"
echo "next:"
echo "  1. write skills/$BUCKET/$NAME/SKILL.md (replace every TODO)"
echo "  2. fill the TODOs in skills/$BUCKET/README.md and agents/openai.yaml"
echo "  3. add the skill to the list in README.md"
echo "  4. run scripts/validate.sh"
