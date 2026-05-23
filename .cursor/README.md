# Cursor configuration – RaFood API

This folder holds Cursor rules and agent prompts so the AI assistant follows project structure and behaves consistently for different tasks.

## Contents

| Path        | Purpose                                                                                                  |
| ----------- | -------------------------------------------------------------------------------------------------------- |
| `rules/`    | Project rules (`.mdc` files) that inject context: stack, domain layout, tests, migrations.               |
| `prompts/`  | Agent instructions: one file per “mode” (feature, explain, review). Use via @-mention or copy into chat. |
| `README.md` | This file.                                                                                               |

See the root [AGENTS.md](../AGENTS.md) for when to use each agent and how to invoke it. When the agent **produces or changes code**, it **automatically** runs quality checks (format, lint, type check, tests) and fixes failures. **agent-boundaries.mdc**: no `migrate`/`rollback`; `create-migration` only with your approval; no `git add`/commit/push; read-only git (`diff`, `status`, `log`) is OK; **dependencies.mdc**: you run `poetry add` and `make build` after lockfile changes. Commands: **Makefile** (`make help`).

______________________________________________________________________

## Rules (`rules/`)

Rules are written in **Markdown with YAML frontmatter** (`.mdc`). Cursor uses them to give the agent project-specific context.

### Files

| File                      | When it applies                             | Content                                                                                                                                                                                                                       |
| ------------------------- | ------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **project-context.mdc**   | Always (`alwaysApply: true`)                | Stack, folder layout, domains, API wiring; **read `docs/` and relevant ADRs** before implementing; quality checks; points to agent-boundaries for migrations/git.                                                             |
| **agent-boundaries.mdc**  | Always (`alwaysApply: true`)                | No migrate/rollback; `create-migration` only with user approval; no git add/commit/push; read-only git OK; **ADRs created only by user**; no Poetry add/install; no deploy unless asked.                                      |
| **dependencies.mdc**      | Always (`alwaysApply: true`)                | New packages: user runs `poetry add` / `--group dev`; user runs `make build` (Compose) or `make build-container` (K8s local) after lockfile changes; agent suggests commands and implements code after install.               |
| **docker-compose.mdc**    | Always (`alwaysApply: true`)                | Default local runtime is Docker Compose; which Make targets need containers up; check `make list-containers` before tests/migrations; do not use `make run`; host vs container commands.                                      |
| **response-language.mdc** | Always (`alwaysApply: true`)                | Reply in pt-BR when the user writes in Portuguese, in English when they write in English; code and identifiers stay in English.                                                                                               |
| **quality-checks.mdc**    | Always (`alwaysApply: true`)                | After generating code: automatically run format, lint, type check, tests and fix failures (`make format`, `make lint-fix`, `make lint-type`, `make test` / `make lint-complete`).                                             |
| **code-design.mdc**       | When editing `src/**/*.py`, `tests/**/*.py` | Clean code: no redundant docstrings/comments, no top-of-file docstrings, good names (no abbreviations), extract helpers, full type hints. When delivering code: explain where/why briefly and add doc references when useful. |
| **domain-structure.mdc**  | When editing `src/**/*.py`                  | Per-domain layout: api, service, repository, models, schemas, deps, exceptions; reference `src/categories/`.                                                                                                                  |
| **tests-structure.mdc**   | When editing `tests/**/*.py`                | Unit vs feature layout, conftest, session/client, factories, naming, fixtures.                                                                                                                                                |
| **migrations.mdc**        | When editing `alembic/**/*.py`              | How to create revisions, do not edit applied ones, env.py and metadata.                                                                                                                                                       |

### Frontmatter

- `description`: Short summary (e.g. for rule picker).
- `globs`: Optional. File pattern so the rule is used when matching files are in context (e.g. `src/**/*.py`).
- `alwaysApply`: If `true`, the rule is always included; if `false` or omitted, it is used when globs match.

______________________________________________________________________

## Prompts (`prompts/`)

Each prompt file defines **one agent mode**. Use them by @-mentioning the file (e.g. `@.cursor/prompts/feature-agent.md`) or by pasting the relevant part into the chat when you start a task.

| File                 | Agent                      | Use when                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| -------------------- | -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **feature-agent.md** | Feature (new, add, modify) | You want the agent to **implement** new code or **add to or modify** existing code (and tests). Works **progressively in the same chat**: keeps context and iterates on follow-ups ("add Y", "change Z"). Follows code-design and quality-checks; explains where/why and adds doc references. For planning without code, use Cursor **Plan** mode. You run `poetry add` and `make build` when new dependencies are needed. Automatically runs format, lint, type check, tests after producing or changing code and fixes failures. |
| **explain-agent.md** | Explain / teach            | Explanations and **how-to implement** proposals aligned with rules/docs/ADRs; may **recommend** user-created ADRs for significant decisions; objective tone; Mermaid; no code or ADR files.                                                                                                                                                                                                                                                                                                                                        |
| **review-agent.md**  | Code review                | You want a **structured review** of code (structure, errors, tests, migrations, clarity, **performance**, **complexity**). No commands; only feedback and suggestions.                                                                                                                                                                                                                                                                                                                                                             |

______________________________________________________________________

## Quick reference

- **“I want to add a new feature”** → Use or mention `prompts/feature-agent.md`. The agent will implement (create, add, or modify code and tests). Use Cursor **Plan** mode for a plan without code.
- **“I need a new Python package”** → You run `poetry add …` (or `--group dev`); then `make build` if using Docker. See **dependencies.mdc**.
- **“Explain X” / “How would I use Y here?”** → Use or mention `prompts/explain-agent.md`. The agent will explain and link to docs, without implementing.
- **“Review this code”** → Use or mention `prompts/review-agent.md`. The agent will review against project rules, conventions, performance, and complexity.

Whenever the agent **creates or changes code**, it will briefly explain **where** each part lives and **why**, stay objective and concise, and add **references to official docs** (FastAPI, SQLModel, Pydantic, pytest, etc.) when useful. After generating code, it will **automatically** run quality checks (format, lint, type check, tests) and fix failures so the code is good.

## Language

Rules and prompts are written in **English** for consistency. Agent replies follow **response-language.mdc**: Portuguese in → pt-BR out; English in → English out. Code and identifiers stay in English.
