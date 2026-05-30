# Code review — RaFood API

## Language

- Write **all review comments in Portuguese (pt-BR)**. Keep code, paths, and identifiers in English.
- This instruction file is in English; your output to the author is not.

## Tone and format

- Be **objective, concise, and direct**: problem → impact → suggestion. No long paragraphs.
- Tag every comment with severity: **critical**, **high**, **medium**, or **low**.
- Grammar, wording, or cosmetic formatting: always **low** — never block a PR for this.

## Project standards (read from the repo)

Before reviewing, **consult these files in the repository** and align feedback with them:

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

## Deprioritize

- Style already enforced by Ruff/pre-commit, unless it hides a real bug.
- Subjective preferences with no functional impact.
- ADRs or new dependencies — mention only for significant undocumented architectural decisions.

## Do not ask the author to run

migrate, deploy, local Newman smoke, or `make agent-checks` — author/CI handles that.
