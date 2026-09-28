# Code review — RaFood API

## Language

- Write **all review comments in Portuguese (pt-BR)**. Keep code, paths, and identifiers in English.
- This instruction file is in English; your output to the author is not.

## Tone and format

- Be **objective, concise, and direct**: problem → impact → suggestion. No long paragraphs.

- Do **not** prefix comments with `[critical]`, `[high]`, `[medium]`, or `[low]`.

- Open every comment with **exactly one** of these lines (Portuguese), matched to how serious the issue is. The emoji is the severity signal — do not add a bracket tag on top:

  | Weight   | Opening line                                               |
  | -------- | ---------------------------------------------------------- |
  | critical | 🚨 Para tudo — isso precisa ser resolvido antes de seguir. |
  | high     | 🔥 Isso pesa: ajusta agora pra não virar problema depois.  |
  | medium   | 👀 Vale uma olhada com carinho.                            |
  | low      | 💡 Só um toque, sem drama.                                 |

- Grammar, wording, or cosmetic formatting: always the 💡 line — never block a PR for this.

- The weight names above are **internal only**. The author sees the opening line, not the label.

## Project standards (read from the repo)

Before reviewing, **consult these files in the repository** and align feedback with them where applicable. Cursor-specific instructions about running commands or grouped output formats do not apply to Copilot Code Review:

- **Primary guide**: `.cursor/prompts/review-agent.md`
- **Cursor rules** (`.cursor/rules/`):
  - `project-context.mdc` — stack, layout, ADRs
  - `domain-structure.mdc` — `api` / `service` / `repository` / `models` / `schemas` / `deps` / `exceptions`
  - `code-design.mdc` — typing, naming, no redundant docstrings
  - `tests-structure.mdc` — unit vs feature, fixtures, naming
  - `smoke-tests.mdc` — when CI smoke (`postman/smoke.postman_collection.json`) should change
  - `migrations.mdc` — Alembic rules
- **ADRs** in `docs/adr/` when the change is architectural.
- **Reference domain**: `src/categories/`.

Do not invent standards beyond what those files and existing code patterns say.

## Review priorities

- Bugs, security, broken contracts
- Missing or weak tests
- Performance and complexity
- Structure and project conventions
- Clarity and maintainability

## What to check

### Errors and security — high/critical

Input validation. Domain exceptions and global handlers. No sensitive data in logs or responses.

### Tests — high/medium

- Changed/new service → unit test in `tests/unit/src/<domain>/` (mocked repository).
- Changed/new endpoint → feature test in `tests/feature/src/<domain>/` (HTTP `/api/v1/...`).
- Names: `test_<action>_<scenario>`. Cover happy path and main error cases.
- HTTP contract changes → check `smoke-tests.mdc`; flag if `postman/smoke.postman_collection.json` should have been updated or would be redundant.

### Performance and complexity — medium/high

N+1 or queries in loops; misuse of async; long or deeply nested functions; avoidable O(n²); over-fetching; missing indexes on frequent queries.

### Migrations — high

Schema changes only via **new** Alembic revisions. Never edit applied revisions. Use `op.*` in `upgrade()`/`downgrade()`; do not import app models inside migrations.

### Code design — medium/low

Full type hints (mypy). Clear names. No redundant docstrings. Short functions; extract helpers. Reuse existing patterns.

## Feature prompts and plans

Files under `docs/feature-prompts/` — including anything in a `plans/` folder — are working notes for the assistant, not the source of truth for the implementation.

- Always the lightest weight. Never use 🚨, 🔥, or 👀 on these files.

- Open with this exact line (it already includes the 💡 tone **and** the “just a heads-up” note), then the observation if it is still useful:

  > 💡 Só um toque, sem drama. Só um ponto de atenção — em feature prompt e plan é normal o texto divergir do que foi implementado.

- Do not ask the author to “fix” a prompt or plan so it matches the code, unless they explicitly changed those docs in the PR and the note would mislead the next session.

## Deprioritize

- Style already enforced by Ruff/pre-commit, unless it hides a real bug.
- Subjective preferences with no functional impact.
- ADRs or new dependencies — mention only for significant undocumented architectural decisions.

## Do not ask the author to run

migrate, deploy, local Newman smoke, or `make agent-checks` — author/CI handles that.
