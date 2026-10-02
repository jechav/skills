#!/usr/bin/env bash
set -euo pipefail

# Checks the invariants described in AGENTS.md. Run before every commit; CI runs it too.

REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"
PLUGIN=".claude-plugin/plugin.json"
errors=0
fail() { echo "error: $*" >&2; errors=$((errors + 1)); }

# Every skill: valid frontmatter, name matches folder, registered, documented.
while IFS= read -r skill_md; do
  dir="$(dirname "$skill_md")"
  folder="$(basename "$dir")"
  bucket_dir="$(dirname "$dir")"

  if [ "$(head -n 1 "$skill_md")" != "---" ]; then
    fail "$skill_md: must start with a --- frontmatter block"
    continue
  fi
  front="$(awk 'NR==1{next} /^---$/{exit} {print}' "$skill_md")"
  name="$(echo "$front" | sed -n 's/^name:[[:space:]]*//p' | tr -d '"'"'")"
  desc="$(echo "$front" | sed -n 's/^description:[[:space:]]*//p')"

  [ "$name" = "$folder" ] || fail "$skill_md: name '$name' must equal folder name '$folder'"
  [[ "$name" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]] || fail "$skill_md: name must be lowercase-hyphenated"
  [ -n "$desc" ] || fail "$skill_md: missing description"
  [ ${#desc} -le 1024 ] || fail "$skill_md: description is ${#desc} chars (max 1024)"
  if grep -q "TODO" "$skill_md"; then fail "$skill_md: still contains TODO"; fi

  jq -e --arg p "./$dir" '.skills | index($p)' "$PLUGIN" > /dev/null \
    || fail "./$dir is not listed in $PLUGIN"
  grep -q "(./$folder/SKILL.md)" "$bucket_dir/README.md" 2>/dev/null \
    || fail "$bucket_dir/README.md does not link $folder"
  grep -q "$dir/SKILL.md" README.md \
    || fail "README.md does not link $dir/SKILL.md"
  [ -f "$dir/agents/openai.yaml" ] || fail "$dir/agents/openai.yaml is missing"
done < <(find skills -name SKILL.md | sort)

# Every plugin.json entry must exist.
while IFS= read -r p; do
  [ -f "$p/SKILL.md" ] || fail "$PLUGIN lists $p but $p/SKILL.md does not exist"
done < <(jq -r '.skills[]' "$PLUGIN")

if command -v claude > /dev/null; then
  claude plugin validate . || fail "marketplace manifest is invalid"
  claude plugin validate "$PLUGIN" || fail "plugin manifest is invalid"
fi

if [ "$errors" -gt 0 ]; then
  echo "$errors problem(s) found" >&2
  exit 1
fi
echo "ok"
