@.cursor/prompts/feature-agent.md

## Context

Based on ADR 009 - Use Kafka for event-driven communication and CDC for real-time data synchronization, add Kafka and Debezium to the project (search for the references and documentation to implement the feature).

Transactional outbox pattern is already implemented. We need to add Kafka and Debezium to the project to achieve the CDC functionality.

Goals:

- Use Kafka for event-driven communication.
- Use Kafka Connect to connect the database to Kafka.
- Use Debezium to read the changes (outbox table) from the database and send them to Kafka.

Requirements:

- Use Docker and Docker Compose to run services.
- Uses Confluent Control Center to monitor the Kafka and Debezium.
- Needs to create topic for product events (created, updated, deleted).
- The event payload should be the product schema (only with after).
- Uses Avro for schema registry.
- Needs to have Kafka Source Connector for the outbox table.

> The events will be consumed by consumers (to be implemented later) or will be used for CDC
> and be upserted to Elastic Search database (to be implemented later).

**Topics must have more than one partition and more than one replica** and the event production must be **ordered** and **idempotent**.

## Logic flow

There's no logic flow for this feature. The goal is to add Kafka and Debezium to the project and make it work with the transactional outbox pattern.

## Acceptance criteria

- Kafka and Debezium will be running in a Docker Compose profile.
- The outbox table will be monitored by Debezium.
- The events will be sent to Kafka topics.
- The events will be consumed by consumers (to be implemented later) or will be used for CDC
- The events will be upserted to Elastic Search database (to be implemented later).

## Extra

- Create a new profile at Docker Compose to run Kafka and Debezium.
- Must create a shell script to create the topics for the product events.

## References

- `docs/adr/009-use-kafka-for-event-driven-communication-and-cdc-for-real-time-data-synchronization.md`
- `src/products` directory and the `Product` entity.
- `src/core/outbox` directory and the `Outbox` entity.
