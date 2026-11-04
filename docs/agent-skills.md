# Agent skills

Skills used by Cursor in this repo live under `.cursor/skills/`. They are part of the project, so a clone already includes them.

When a skill is installed or removed, update this file in the same change: one row in the table, and a note of how that skill was installed. Each skill has its own install. Do not document one command as if it covered every skill.

| Skill                                                         | What it does                                                                                     | Reference                                                                                       |
| ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------- |
| [domain-analysis](../.cursor/skills/domain-analysis/SKILL.md) | Maps business domains in the codebase and suggests bounded contexts (Core, Supporting, Generic). | [Tech Leads Club — domain-analysis](https://agent-skills.techleads.club/skills/domain-analysis) |

## How each one was installed

### domain-analysis

From the Tech Leads Club catalog, into this repo, Cursor only:

```bash
npx @tech-leads-club/agent-skills install -s domain-analysis -a cursor
```

Files landed in `.cursor/skills/domain-analysis/`. Open a new chat after installing so the agent picks the skill up.

## Where to look for more

- [awesome-cursor-skills](https://github.com/spencerpauly/awesome-cursor-skills): curated list of Cursor skills.
- [skills.sh](https://www.skills.sh): directory of agent skills, with install commands per skill.

Picking one from either list still means a row in the table above and a note of how that skill was installed.
