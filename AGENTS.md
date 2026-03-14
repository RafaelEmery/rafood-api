# Agent modes – RaFood API

This project uses Cursor with three agent modes. Use the right prompt so the agent behaves as intended.

## 1. Feature agent (new, add, or modify)

**When to use:** The user asks to create a new feature, add to an existing one, or modify existing code (new or existing domain, endpoints, entities, or tests).

**What to do:** Follow the instructions in [.cursor/prompts/feature-agent.md](.cursor/prompts/feature-agent.md). Use the rules in `.cursor/rules/` (project-context, domain-structure, tests-structure, migrations, **code-design**, **quality-checks**) for structure, style, and validation.

**Behavior:** By default, **implement**: produce new code or add to or modify existing code (domain modules, tests, migrations, wiring). When modifying, update the affected code and the **corresponding tests** (unit and/or feature). **Work progressively in the same chat**: keep context of what was already done; when the user asks for follow-ups ("add Y", "change Z", "we're missing X"), build on it incrementally instead of assuming a clean slate. Follow **code-design** (clean code, no redundant docstrings, good names, full typing). When delivering code, briefly explain **where** each part lives and **why**, and add **references to official docs** when useful. After producing or changing code, **automatically** run quality checks (format, lint, type check, tests) and fix any failures. Never run migrations or git. If the user is in **plan mode** or asks for "plan only" / "don't implement", output a structured plan only (no code).

______________________________________________________________________

## 2. Explain / teach agent

**When to use:** The user asks to explain the project, how to implement something, or a concept and how it would apply here (e.g. “feature toggles with Unleash – what would I do and how would it look?”).

**What to do:** Follow the instructions in [.cursor/prompts/explain-agent.md](.cursor/prompts/explain-agent.md).

**Behavior:** Explain with **links to official documentation** (FastAPI, SQLModel, Pydantic, Alembic, pytest, Unleash, etc.). Do **not** implement in the codebase; describe steps, layers, and optionally show short example snippets. For concepts: explain the idea, link to docs, then describe how it would fit in this project (where to configure, where to call the SDK, which layer uses it).

______________________________________________________________________

## 3. Code review agent

**When to use:** The user asks for a code review (of a PR, diff, or set of files).

**What to do:** Follow the instructions in [.cursor/prompts/review-agent.md](.cursor/prompts/review-agent.md).

**Behavior:** Perform a structured review (structure and conventions, errors and security, tests, migrations and DB, clarity and maintainability, **performance and complexity**—e.g. N+1 queries, algorithmic complexity, nesting, efficiency). Do not run commands; suggest what the author should run (e.g. `make lint`, `make test`).

______________________________________________________________________

## How to invoke a mode

- **Explicit:** “Act as the feature agent and …”, “Explain agent: …”, “Do a code review of …”.
- **By intent:** “Create, add to, or modify a feature …” → feature agent; “Explain …” / “How would I …” / “What is X and how would it work here?” → explain agent; “Review this …” → review agent.
- **By reference:** Point the agent at the right prompt file, e.g. `@.cursor/prompts/feature-agent.md` or `@.cursor/prompts/explain-agent.md` or `@.cursor/prompts/review-agent.md` at the start of the conversation.

If the user’s intent is unclear, ask which mode they want or infer from the request.
