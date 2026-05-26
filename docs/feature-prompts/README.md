# Feature Prompts

This directory contains the feature prompts for the RaFood API used for communication with the Cursor AI assistant.

The goal here is to document the prompts used for the Cursor AI assistant to understand the context of the project and the codebase

## Structure

Has the <feature-name>.md file for each feature or change.

### ADRs and documentation references

- [restaurants-and-offers-near-by](./restaurants-and-offers-near-by/): [008-add-postgis-and-gist-index.md](../adr/008-add-postgis-and-gist-index.md)

## Base feature prompt

### Simple feature prompt example

```text
@.cursor/prompts/feature-agent.md

<Add a new | Add to existing | Modify existing> <domain/feature>: <short description>. Follow the existing domain structure (api, service, repository, models, schemas, deps, exceptions). Create or update unit and feature tests as needed; add a migration if needed. Explain where each part lives and why.
```

### Elaborate feature prompt example

```text
@.cursor/prompts/feature-agent.md

## Context

<Add a new | Add to existing | Modify existing> <domain/feature>: <short description>. Follow the existing domain structure (api, service, repository, models, schemas, deps, exceptions). Create or update unit and feature tests as needed; add a migration if needed. Explain where each part lives and why.

## Logic flow

> Some logic flow to the feature.

## Acceptance criteria

> Some acceptance criteria to the feature.

## Extra

> Extra tasks

## References

> Some ADR, documentation or any other reference to the feature.
```
