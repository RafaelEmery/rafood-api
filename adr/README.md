# Architecture Decision Records (ADR)

According to [adr.github.io](https://adr.github.io/) an `Architectural Decision (AD)` is a justified design choice that addresses a functional or non-functional requirement that is architecturally significant.

> An Architecture Decision Record (ADR) is a document that captures an important architecture decision made along with its context and consequences.

Based on [architecture-decision-record](https://github.com/joelparkerhenderson/architecture-decision-record) on GitHub.

## Records name

The names must follow a `XXX-some-change-name` pattern and all must use Markdown (`.md`).

It also must have a present tense imperative verb phrase.

Example: `001-choose-database.md` or `002-improve-exception-handling.md`

## Records structure

Based on [Michael Nygard template](https://github.com/joelparkerhenderson/architecture-decision-record/tree/main/locales/en/templates/decision-record-template-by-michael-nygard)

```
# Title

## Context

What is the issue that we're seeing that is motivating this decision or change?

## Decision

What is the change that we're proposing and/or doing?

## Consequences

What becomes easier or more difficult to do because of this change?

## References

Docs, links or any other references to this change.
```
