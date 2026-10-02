# skills

Agent skills I use, packaged so they work with **Claude** (Code, Desktop, claude.ai), **Codex / ChatGPT**, **Cursor**, **GitHub Copilot**, **Gemini CLI** and any other tool that supports the open [Agent Skills](https://agentskills.io) format.

A skill is a folder with a `SKILL.md` (instructions plus a `description` that tells the agent when to use it). Some skills also include `references/` (docs the agent reads when it needs them) and `scripts/` (helpers the agent runs).

## Skills

### Annotation

- **[website-judgment-auditor](./skills/annotation/website-judgment-auditor/SKILL.md)**: Audit hand-written Website A vs Website B justifications against the task rules, without rewriting them. Manual-only: name the skill, or paste the `Request:` / `Selected:` / `Aesthetics:` / `Functionality:` / `Overall:` template.

## Install

Pick one method per tool. If you install the same skill twice, the agent sees duplicates.

<details open>
<summary><strong>Claude Code (plugin, auto-updates)</strong></summary>

```bash
claude plugin marketplace add jechav/skills
claude plugin install jechav-skills@jechav
```

Or, from inside a session: `/plugin marketplace add jechav/skills`, then `/plugin install jechav-skills@jechav`.

</details>

<details>
<summary><strong>Codex, Cursor, Copilot, Gemini CLI and 40+ other agents</strong></summary>

```bash
npx skills@latest add jechav/skills
```

The installer asks which skills to install and which agents to install them for. To install just one skill:

```bash
npx skills@latest add jechav/skills --skill website-judgment-auditor
```

The skills are copied into your project (or into your home directory with `-g`) as editable files. Run `npx skills update` to pull new versions.

</details>

<details>
<summary><strong>claude.ai, Claude Desktop, and ChatGPT (upload a zip)</strong></summary>

1. Download `<skill-name>.zip` from the [latest release](https://github.com/jechav/skills/releases/latest).
2. **Claude**: go to Settings, then Capabilities, then Skills, and upload the zip.
   **ChatGPT**: if your plan supports skills, upload the same zip in the skills settings.

</details>

<details>
<summary><strong>Any other chatbot (copy and paste)</strong></summary>

Paste the contents of the skill's `SKILL.md` and its `references/*.md` into a Project's or custom GPT's instructions. The `scripts/` only automate checks that `SKILL.md` already describes in prose, so the skill still works without them, just less precisely.

</details>

## Adding a skill

See [CONTRIBUTING.md](./CONTRIBUTING.md). Short version:

```bash
scripts/new-skill.sh <bucket> <skill-name>   # scaffold and register
scripts/validate.sh                          # check everything is wired up
```

## License

[MIT](./LICENSE)
