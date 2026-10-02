# Adding a skill

Every skill lives at `skills/<bucket>/<skill-name>/`. A bucket is a category folder such as `annotation/` or `productivity/`. To start a new bucket, use a new name; the script creates the folder.

## 1. Scaffold

```bash
scripts/new-skill.sh <bucket> <skill-name>
```

This copies `templates/skill/` and registers the new skill in `.claude-plugin/plugin.json` and `skills/<bucket>/README.md`. Skill names use lowercase letters, digits and hyphens, and must match the folder name.

If you already have a skill (for example one exported from claude.ai), run the script anyway, then replace the generated `SKILL.md` with yours and copy in its other files.

## 2. Write `SKILL.md`

```markdown
---
name: my-skill
description: What it does. Use when the user ... Do NOT use for ...
---

# My Skill

Instructions for the agent.
```

- **`description` is the most important line.** The agent reads only this line when deciding whether to load the skill. Name the trigger phrases, the inputs it applies to, and what it should *not* trigger on. Maximum 1024 characters.
- Keep `SKILL.md` short (well under 500 lines). Move long material into `references/*.md` and say in `SKILL.md` when to read each file.
- Put deterministic work (parsing, counting, validation) in `scripts/`. Call scripts by relative path, for example `python scripts/check.py`.
- Write for any user: no personal names, secrets, or private or proprietary material.
- To make a skill **manual-only**:
  - **Claude Code**: add `disable-model-invocation: true` to the frontmatter.
  - **Codex**: set `policy.allow_implicit_invocation: false` in `agents/openai.yaml`.

## 3. Fill in the listings

- `agents/openai.yaml`: `display_name` and `short_description` (used by Codex and ChatGPT).
- `skills/<bucket>/README.md`: replace the TODO with one line describing the skill.
- `README.md`: add the skill under its bucket heading, linking to its `SKILL.md`.

## 4. Test locally

```bash
scripts/validate.sh       # frontmatter, names, listings, plugin manifest
scripts/link-skills.sh    # symlink every skill into ~/.claude/skills and ~/.agents/skills
```

Open a new Claude Code (or Codex) session and try both a prompt that **should** trigger the skill and one that **shouldn't**.

## 5. Release

1. Bump `version` in `.claude-plugin/plugin.json`. Claude Code users only see an update when this number changes.
2. Commit, open a PR, and merge once CI passes.
3. Tag the release:

   ```bash
   git tag v0.2.0 && git push origin v0.2.0
   ```

   The `release` workflow zips every skill and attaches the zips to a GitHub Release, ready for claude.ai and ChatGPT upload.
