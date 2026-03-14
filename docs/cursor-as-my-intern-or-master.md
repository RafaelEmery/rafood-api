# Cursor as my intern (or master)

Proposed at [Add Cursor as my Intern ADR](adr/008-add-cursor-as-my-intern.md).

## Overview

This project uses Cursor with **rules** and **agent prompts** so the AI follows the codebase structure, writes clean code, runs quality checks after producing or changing code, and never touches git or migrations. Three modes are available: **feature** (new, add, or modify—implement or plan), **explain / teach**, and **code review**.

Configuration lives under [.cursor/](../.cursor/) and the root [AGENTS.md](../AGENTS.md). Use the prompts below to get the most out of the agent.

## How it works

- **Rules** (`.cursor/rules/*.mdc`): Injected context—stack, domain layout, tests, migrations, code style, quality checks. Some apply always, others when you edit matching files.
- **Prompts** (`.cursor/prompts/*.md`): One file per “agent”. Mention them in chat (e.g. `@.cursor/prompts/feature-agent.md`) or paste the model prompt so the agent behaves as that mode.
- **AGENTS.md**: Describes when to use each mode and how to invoke it.

When the agent **produces or changes code**, it automatically runs format, lint, type check, and tests and fixes failures. It never runs migrations or git commands.

## Model prompts

Copy-paste into the chat (or combine with @-mention of the prompt file). Replace the placeholders with your case.

### Feature (new, add, or modify – implement)

Use when you want the agent to create new code or add to or modify existing code (and the corresponding tests), following the project structure, then run quality checks.

```text
@.cursor/prompts/feature-agent.md

<Add a new | Add to existing | Modify existing> <domain/feature>: <short description>. Follow the existing domain structure (api, service, repository, models, schemas, deps, exceptions). Create or update unit and feature tests as needed; add a migration if needed. Explain where each part lives and why.
```

Example (new):

```text
@.cursor/prompts/feature-agent.md

Add a new "orders" context: list and create orders linked to a restaurant and optional products. Follow the existing domain structure, write unit and feature tests, and add a migration. Explain where each part lives and why.
```

Example (modify):

```text
@.cursor/prompts/feature-agent.md

Modify existing offers: add an optional "valid_until" field to the offer model and API. Update the service, repository, schemas, and the corresponding unit and feature tests. Explain where you changed things and why.
```

### Feature (plan only)

Use when you want a structured plan with no code (for something new, or to add/modify existing).

```text
@.cursor/prompts/feature-agent.md

Plan mode: I want to <add | modify> <short description>. Give me a structured plan only (files to create or change, models, migration steps if needed, API, services, tests to add or modify, wiring). Do not implement.
```

### Code review

Use to get a structured review (structure, errors, tests, migrations, clarity, performance, complexity).

```text
@.cursor/prompts/review-agent.md

Review this code: <paste or @-mention files/diff>. Check structure, errors, tests, migrations, clarity, performance and complexity. Be direct and suggest what to fix; remind me to run make lint-complete and make test.
```

Example:

```text
@.cursor/prompts/review-agent.md

Review the changes in src/offers/ and tests/feature/src/offers/. Check structure, errors, tests, migrations, clarity, performance and complexity.
```

### Explain / teach

Use to understand the project, how to implement something, or a concept and how it would apply here. No code changes; the agent will add doc links.

```text
@.cursor/prompts/explain-agent.md

Explain <topic>: <your question>. Do not implement; add links to official docs where relevant.
```

Examples:

```text
@.cursor/prompts/explain-agent.md

Explain how dependency injection works in this project and where get_session is used. Add links to FastAPI docs.
```

```text
@.cursor/prompts/explain-agent.md

I want to use feature toggles with Unleash. What is it, how would it fit in this project, and where would config and SDK calls go? Do not implement; only describe and link to docs.
```

## Tips

- Start the conversation with the @-mention of the prompt file so the agent loads the right mode.
- For features (new, add, or modify), be specific about the domain name and scope so the agent follows the right structure and updates the right code and tests. In the **same chat** you can iterate: e.g. "add X", then "we're missing Y", then "I want Z different" — the agent keeps context and builds on what was already done.
- For reviews, point to the exact files or diff you care about.
- For explain, ask one clear question; you can follow up in the same thread.

## References

- [.cursor/README.md](../.cursor/README.md) – Rules and prompts overview.
- [AGENTS.md](../AGENTS.md) – When to use each agent and how to invoke it.
