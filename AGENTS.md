# Agent modes – RaFood API

This project uses Cursor with three agent modes. Use the right prompt so the agent behaves as intended.

## 1. Feature agent (new, add, or modify)

**When to use:** The user asks to create a new feature, add to an existing one, or modify existing code (new or existing domain, endpoints, entities, or tests).

**What to do:** Follow the instructions in [.cursor/prompts/feature-agent.md](.cursor/prompts/feature-agent.md). Use the rules in `.cursor/rules/` (project-context, domain-structure, tests-structure, migrations, **code-design**, **quality-checks**, **smoke-tests**) for structure, style, and validation.

**Behavior:** By default, **implement**: produce new code or add to or modify existing code (domain modules, tests, migrations, wiring). When modifying, update the affected code and the **corresponding tests** (unit and/or feature). For **public API** changes, **evaluate and update the CI smoke collection** per **smoke-tests.mdc** (`postman/smoke.postman_collection.json`, happy path only); say in the summary whether smoke was added, updated, or skipped. **Do not run** Newman smoke locally — CI runs it in GitHub Actions. **Work progressively in the same chat**: keep context of what was already done; when the user asks for follow-ups ("add Y", "change Z", "we're missing X"), build on it incrementally instead of assuming a clean slate. Follow **code-design** (clean code, no redundant docstrings, good names, full typing). When delivering code, briefly explain **where** each part lives and **why**, and add **references to official docs** when useful. After producing or changing code, **automatically** run **`make agent-checks`** (see **quality-checks.mdc**) and fix any failures. Follow **agent-boundaries.mdc** and **dependencies.mdc**: no migrate/rollback; `create-migration` only with user approval; no git add/commit/push; user runs `poetry add` and `make build` when a new package is needed; read-only git for context is OK. For planning without code, use Cursor **Plan** mode.

______________________________________________________________________

## 2. Explain / teach agent

**When to use:** The user asks to explain the project, how to implement something, or a concept and how it would apply here (e.g. “feature toggles with Unleash – what would I do and how would it look?”).

**What to do:** Follow the instructions in [.cursor/prompts/explain-agent.md](.cursor/prompts/explain-agent.md).

**Behavior:** **Objective and concise** answers; use Mermaid when it clarifies flows. Read **project rules**, **docs**, and **ADRs**; “how to implement” proposals must follow the same conventions as the feature agent (domain layout, tests, code-design, boundaries). **Recommend** (do not create) an ADR when a decision is architecturally significant—only the user creates ADRs. Link to official docs (FastAPI, SQLModel, Pydantic, Alembic, pytest, etc.). Do **not** implement in the codebase.

______________________________________________________________________

## 3. Code review agent

**When to use:** The user asks for a code review (of a PR, diff, or set of files).

**What to do:** Follow the instructions in [.cursor/prompts/review-agent.md](.cursor/prompts/review-agent.md).

**Behavior:** Perform a structured review (structure and conventions, errors and security, tests—including **smoke** per **smoke-tests.mdc** when the API changed, migrations and DB, clarity and maintainability, **performance and complexity**—e.g. N+1 queries, algorithmic complexity, nesting, efficiency). Run **`make agent-checks`** (optional `t='tests/...'`) and report pass/fail in the review. Do not run migrate, deploy, or git commands.

______________________________________________________________________

## How to invoke a mode

- **Explicit:** “Act as the feature agent and …”, “Explain agent: …”, “Do a code review of …”.
- **By intent:** “Create, add to, or modify a feature …” → feature agent; “Explain …” / “How would I …” / “What is X and how would it work here?” → explain agent; “Review this …” → review agent.
- **By reference:** Point the agent at the right prompt file, e.g. `@.cursor/prompts/feature-agent.md` or `@.cursor/prompts/explain-agent.md` or `@.cursor/prompts/review-agent.md` at the start of the conversation.

If the user’s intent is unclear, ask which mode they want or infer from the request.
