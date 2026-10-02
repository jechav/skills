This repo publishes agent skills in the open Agent Skills format. Human-facing instructions are in [CONTRIBUTING.md](./CONTRIBUTING.md). The rules below are the invariants that `scripts/validate.sh` enforces.

- Every skill lives at `skills/<bucket>/<skill-name>/SKILL.md`. The frontmatter `name` equals the folder name (lowercase, hyphenated) and `description` is at most 1024 characters.
- Create new skills with `scripts/new-skill.sh <bucket> <skill-name>`. Don't hand-copy folders.
- Every skill must be:
  - listed in `.claude-plugin/plugin.json`'s `skills` array
  - linked from `skills/<bucket>/README.md`
  - linked from the top-level `README.md` under its bucket heading
  - shipped with an `agents/openai.yaml`
- When removing or renaming a skill, update all four places above.
- Manual-only skills set `policy.allow_implicit_invocation: false` in `agents/openai.yaml`. Set `disable-model-invocation: true` in the frontmatter only if the skill should never auto-trigger in Claude.
- Skills are public: no personal names, credentials, or proprietary or NDA material. Write for "the user".
- Keep `SKILL.md` lean and move long material into `references/`.
- Bump `version` in `.claude-plugin/plugin.json` whenever a shipped skill changes.
- Run `scripts/validate.sh` before committing.
