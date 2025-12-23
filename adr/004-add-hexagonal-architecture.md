# Title

Status: `WIP`

## Context

- The current architecture (one folder for each entity) causes a lot of `api.py` or `models.py` (and others) files.
- Coupled dependencies and infrastructure (e.g. database as Postgres).
- Testing only on APIs and not much of unit tests.

## Decision

Refactor into a more *"hexagonalish"* or *"hexagonal-like"* architecture.

Separate *ports and adapters* using dependency inversion principle and organize project files and folders based on Hexagonal Architecture

## Consequences

- Better separation between domain, application and infrastructure
- The application is more reliable to make changes
- Better testing between all the components

## References

- [Hexagonal Architecture in Python](https://medium.com/@augustomarinho/arquitetura-hexagonal-no-python-ae08b108ac12)
- [Ports and Adapters Architecture](https://medium.com/bemobi-tech/ports-adapters-architecture-ou-arquitetura-hexagonal-b4b9904dad1a)
- [Hexagonal Architecture in Python - With Project](https://medium.com/@miks.szymon/hexagonal-architecture-in-python-e16a8646f000)
- [Hexagonal FastAPI Boilerplate](https://github.com/Mingbling1/hexagonal-fastapi-boilerplate/tree/main)
