@.cursor/prompts/feature-agent.md

## Context

Add Transactional Outbox pattern to the project.

Follow the existing domain structure (api, service, repository, models, schemas, deps, exceptions). Create or update unit and feature tests as needed; add a migration if needed. Explain where each part lives and why.

> Important: the events publishing will be handled later by CDC (Change Data Capture) via Debezium, don\`t worry about it now.

The first applied entity will be the `Product` entity.

## Logic flow

New table `outbox` to store the events to be published to Kafka.

When creating a new entity (Product in this case), the event should be stored in the outbox table.
When updating an entity (Product in this case), the event should be stored in the outbox table.
When deleting an entity (Product in this case), the event should be stored in the outbox table.

If the transaction fails, the event should not be published and the transaction should be rolled back.

**Atomicity should be maintained between the entity operation and the outbox table update.**

Read the project structure, the database files, the core directory and domain structure to understand the project and the entities.

## Acceptance criteria

- The outbox table should be created with the correct schema.
- The outbox table should be used to store the events to be published to Kafka.
- The outbox table should be updated when the entity is created, updated or deleted.
- If the transaction fails, the event should not be published and the transaction should be rolled back.
- When creating a new product, the event should be stored in the outbox table.
- When updating a product, the event should be stored in the outbox table.
- When deleting a product, the event should be stored in the outbox table.

## Extra

- Search for official references and documentation to decide about the outbox table schema and show me the references.
- Implement tests and migrations to create the outbox table. You can run lint and tests but not migrations.
- The implementation plan should be created at `plans` directory, to record the steps and decisions made during the implementation.

## References

- `009-add-cdc-transactional-outbox-with-kafka.md`
- `src/products` directory and the `Product` entity.
