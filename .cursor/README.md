# Cursor configuration – RaFood API

This folder holds Cursor rules and agent prompts so the AI assistant follows project structure and behaves consistently for different tasks.

## Contents

| Path        | Purpose                                                                                                  |
| ----------- | -------------------------------------------------------------------------------------------------------- |
| `rules/`    | Project rules (`.mdc` files) that inject context: stack, domain layout, tests, migrations.               |
| `prompts/`  | Agent instructions: one file per “mode” (feature, explain, review). Use via @-mention or copy into chat. |
| `README.md` | This file.                                                                                               |

See the root [AGENTS.md](../AGENTS.md) for when to use each agent and how to invoke it. When the agent **produces or changes code**, it **automatically** runs quality checks (format, lint, type check, tests) to ensure the code is good, and fixes any failures. It **never** runs migrations or git (no commit, push, etc.). All commands are in the project **Makefile** (`make help`).

______________________________________________________________________

## Rules (`rules/`)

Rules are written in **Markdown with YAML frontmatter** (`.mdc`). Cursor uses them to give the agent project-specific context.

### Files

| File                     | When it applies                             | Content                                                                                                                                                                                                                       |
| ------------------------ | ------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **project-context.mdc**  | Always (`alwaysApply: true`)                | Stack, folder layout, response language, domain list, API prefix, ADRs, and “when generating code run quality checks automatically; never migrations or git”.                                                                 |
| **quality-checks.mdc**   | Always (`alwaysApply: true`)                | After generating code: automatically run format, lint, type check, tests and fix failures (`make format`, `make lint-fix`, `make lint-type`, `make test` / `make lint-complete`).                                             |
| **code-design.mdc**      | When editing `src/**/*.py`, `tests/**/*.py` | Clean code: no redundant docstrings/comments, no top-of-file docstrings, good names (no abbreviations), extract helpers, full type hints. When delivering code: explain where/why briefly and add doc references when useful. |
| **domain-structure.mdc** | When editing `src/**/*.py`                  | Per-domain layout: api, service, repository, models, schemas, deps, exceptions; reference `src/categories/`.                                                                                                                  |
| **tests-structure.mdc**  | When editing `tests/**/*.py`                | Unit vs feature layout, conftest, session/client, factories, naming, fixtures.                                                                                                                                                |
| **migrations.mdc**       | When editing `alembic/**/*.py`              | How to create revisions, do not edit applied ones, env.py and metadata.                                                                                                                                                       |

### Frontmatter

- `description`: Short summary (e.g. for rule picker).
- `globs`: Optional. File pattern so the rule is used when matching files are in context (e.g. `src/**/*.py`).
- `alwaysApply`: If `true`, the rule is always included; if `false` or omitted, it is used when globs match.

______________________________________________________________________

## Prompts (`prompts/`)

Each prompt file defines **one agent mode**. Use them by @-mentioning the file (e.g. `@.cursor/prompts/feature-agent.md`) or by pasting the relevant part into the chat when you start a task.

| File                 | Agent                      | Use when                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| -------------------- | -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **feature-agent.md** | Feature (new, add, modify) | You want the agent to **implement** new code or **add to or modify** existing code (and tests). Works **progressively in the same chat**: keeps context and iterates on follow-ups ("add Y", "change Z"). Follows code-design and quality-checks; explains where/why and adds doc references. Use **plan mode** or "plan only" for a plan only. Automatically runs format, lint, type check, tests after producing or changing code and fixes failures. |
| **explain-agent.md** | Explain / teach            | You want **explanations** of the project, how to implement something, or a concept and how it would apply here (e.g. Unleash feature toggles). With doc links; no code changes.                                                                                                                                                                                                                                                                         |
| **review-agent.md**  | Code review                | You want a **structured review** of code (structure, errors, tests, migrations, clarity, **performance**, **complexity**). No commands; only feedback and suggestions.                                                                                                                                                                                                                                                                                  |

______________________________________________________________________

## Quick reference

- **“I want to add a new feature”** → Use or mention `prompts/feature-agent.md`. The agent will implement (create, add, or modify code and tests). Say **"plan mode"** or **"plan only"** if you want just a plan with no code.
- **“Explain X” / “How would I use Y here?”** → Use or mention `prompts/explain-agent.md`. The agent will explain and link to docs, without implementing.
- **“Review this code”** → Use or mention `prompts/review-agent.md`. The agent will review against project rules, conventions, performance, and complexity.

Whenever the agent **creates or changes code**, it will briefly explain **where** each part lives and **why**, stay objective and concise, and add **references to official docs** (FastAPI, SQLModel, Pydantic, pytest, etc.) when useful. After generating code, it will **automatically** run quality checks (format, lint, type check, tests) and fix failures so the code is good.

## Language

Rules and prompts are written in **English** for consistency. The agent may respond in **English** or **Portuguese (pt-BR)**. **English is preferred**, but **pt-BR is also fine**—you can ask in either language and Cursor will handle it; the agent may reply in the same language you used or in English.
