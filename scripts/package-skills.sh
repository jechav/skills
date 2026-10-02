#!/usr/bin/env bash
set -euo pipefail

# Build one <skill-name>.zip per skill into dist/, with the skill folder at the
# zip root. This is the format claude.ai / Claude Desktop skill upload expects.

REPO="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$REPO/dist"
rm -rf "$OUT" && mkdir -p "$OUT"

while IFS= read -r skill_md; do
  dir="$(dirname "$skill_md")"
  name="$(basename "$dir")"
  (cd "$(dirname "$dir")" && zip -qr "$OUT/$name.zip" "$name" -x '*.DS_Store' -x '*/__pycache__/*')
  echo "packaged dist/$name.zip"
done < <(find "$REPO/skills" -name SKILL.md | sort)
