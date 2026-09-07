# Debezium outbox source connector

`outbox-source.json` is the Kafka Connect configuration that turns rows of the `outbox` table into Kafka events. It is registered automatically by `../setup.sh`, which runs in the one-shot `kafka-setup` container of the `kafka` Compose profile.

The file holds **only the connector config object** (not `{"name": ..., "config": ...}`) because `setup.sh` sends it with `PUT /connectors/rafood-outbox-connector/config`, which creates or updates the connector. `POST /connectors` would return `409 Conflict` on the second run.

The file has no comments because Kafka Connect rejects non-standard JSON. Every property is explained below instead.

## Pipeline

```text
API write (product + outbox row, one transaction)
  -> Postgres WAL (wal_level=logical)
  -> Debezium Postgres connector (replication slot debezium_outbox)
  -> EventRouter SMT (unwraps payload, routes by event type)
  -> Kafka topic, Avro value registered in Schema Registry
```

Topics created by `setup.sh`, one per outbox `type` value:

- `outbox.event.ProductCreated`
- `outbox.event.ProductUpdated`
- `outbox.event.ProductDeleted`

Each has 3 partitions, replication factor 1, `cleanup.policy=delete`. The message key is the product UUID (`aggregateid`), the value is the product snapshot from the outbox `payload`, and `id` / `eventType` travel as headers.

## Properties

### Source database

| Property                                                               | Why it matters                                                                                                                                                      |
| ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `connector.class`                                                      | Selects the Debezium PostgreSQL source connector installed in the Connect image.                                                                                    |
| `plugin.name=pgoutput`                                                 | Native logical decoding output plugin of PostgreSQL 10+, so no extra plugin is installed in the database image.                                                     |
| `database.hostname=database`                                           | Compose service name of Postgres; credentials are rendered by `setup.sh` from the `DB_*` env vars.                                                                  |
| `slot.name=debezium_outbox`                                            | Replication slot that remembers the WAL position. Postgres keeps WAL until the slot advances, so a connector deleted without dropping the slot makes the disk grow. |
| `publication.name=dbz_outbox` + `publication.autocreate.mode=filtered` | Debezium creates a publication limited to the tables in `table.include.list`, instead of publishing every table.                                                    |
| `table.include.list=public.outbox`                                     | The outbox table is the only source of change events; domain tables are never captured.                                                                             |
| `topic.prefix=rafood`                                                  | Prefix of the raw CDC topic name (`rafood.public.outbox`) before the SMT rewrites it.                                                                               |
| `snapshot.mode=initial`                                                | On first start, existing outbox rows are emitted once, then streaming continues from the WAL.                                                                       |
| `tombstones.on.delete=false`                                           | Deleting old outbox rows (cleanup) must not emit tombstones that consumers would read as domain deletions.                                                          |
| `heartbeat.interval.ms=10000`                                          | With a quiet outbox but a busy database, heartbeats let the slot advance; without them WAL accumulates.                                                             |

### Routing (outbox pattern)

| Property                                                                    | Why it matters                                                                                                                                         |
| --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `transforms.outbox.type=io.debezium.transforms.outbox.EventRouter`          | Turns the raw CDC envelope (`before`/`after`/`source`/`op`) into a plain event whose value is the outbox `payload`.                                    |
| `transforms.outbox.table.expand.json.payload=true`                          | Expands the JSONB `payload` into a real record with fields, instead of one escaped JSON string. Required for Avro to carry the product fields.         |
| `transforms.outbox.route.by.field=type`                                     | Routes on the `type` column, producing one topic per event type. Default would be `aggregatetype`, i.e. a single `outbox.event.product` topic.         |
| `transforms.outbox.route.topic.replacement`                                 | Topic name template; `${routedByValue}` is the value of the routing field.                                                                             |
| `transforms.outbox.table.field.event.key=aggregateid`                       | Kafka message key. Same product always hashes to the same partition, which is what preserves order per product.                                        |
| `transforms.outbox.table.fields.additional.placement=type:header:eventType` | Copies the event type into a header, so a consumer reading several topics can branch without parsing the topic name.                                   |
| `predicates.isOutboxChange.*` + `transforms.outbox.predicate`               | The SMT only runs on `rafood.public.outbox` records. Without the predicate, heartbeat and transaction-metadata messages would hit the router and fail. |

### Serialization and topic creation

| Property                                                  | Why it matters                                                                                                                                                                                                                          |
| --------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `value.converter=io.confluent.connect.avro.AvroConverter` | Avro on the wire, with the schema registered in Schema Registry, so consumers get validated and versioned payloads.                                                                                                                     |
| `value.converter.schema.registry.url`                     | Where the schema is registered/fetched. Connect fails to produce if it is unreachable.                                                                                                                                                  |
| `key.converter=StringConverter`                           | The key is the product UUID as text, readable in Control Center and in console consumers.                                                                                                                                               |
| `topic.creation.default.*`                                | The broker runs with `auto.create.topics.enable=false`, so Connect creates any topic the connector still needs (for example the heartbeat topic) with 3 partitions and RF 1. The three product topics are pre-created by `../setup.sh`. |
| `errors.log.enable` / `errors.log.include.messages`       | Failed records are logged with their content, which is what makes `make logs container=connect` useful while learning.                                                                                                                  |

## Known trade-offs in this setup

**Ordering across event types is not guaranteed.** Kafka orders messages per partition, and there is no ordering between topics. With three topics, a consumer can see `ProductDeleted` before the `ProductUpdated` that came first in the database. Order per product is preserved *within* each topic thanks to the key.

Mitigation for future consumers and the Elasticsearch sink: the payload carries `updated_at`, so writes can be applied version-aware (ignore a payload older than the stored document) and a delete can be treated as terminal. Routing all types to a single topic (`route.by.field=aggregatetype`) is the alternative that restores total order per product.

**Replication factor is 1.** The profile runs a single broker, and the replication factor can never exceed the broker count. There is no replica durability: if the broker loses its volume, the events are gone. To move to RF 3, add two more brokers to the `kafka` service definition (distinct `KAFKA_NODE_ID` and controller quorum voters), then raise `REPLICATION_FACTOR` in `../setup.sh`, `topic.creation.default.replication.factor` here, and the `*_REPLICATION_FACTOR` variables of Kafka, Connect, Schema Registry and Control Center in `docker-compose.yml`.

**`wal_level=logical` needs a Postgres restart.** It is set as a `command` flag on the `database` service. An already running container keeps the old value until it is recreated (`docker compose up -d database`); the data volume is not affected.

## Verifying

```bash
# Connector state and tasks
curl -s localhost:8083/connectors/rafood-outbox-connector/status | jq

# Registered Avro schemas
curl -s localhost:8081/subjects

# Read the events (from inside the broker container)
docker compose exec kafka kafka-console-consumer \
  --bootstrap-server kafka:29092 \
  --topic outbox.event.ProductCreated \
  --from-beginning --property print.key=true
```

For the Avro value in a readable form, use `kafka-avro-console-consumer` from the Schema Registry container:

```bash
docker compose exec schema-registry kafka-avro-console-consumer \
  --bootstrap-server kafka:29092 \
  --property schema.registry.url=http://schema-registry:8081 \
  --topic outbox.event.ProductCreated --from-beginning
```

Control Center (topics, throughput, connector status) runs at `http://localhost:9021`.

## References

- [Debezium Outbox Event Router](https://debezium.io/documentation/reference/stable/transformations/outbox-event-router.html)
- [Debezium connector for PostgreSQL](https://debezium.io/documentation/reference/stable/connectors/postgresql.html)
- [Kafka Connect REST API](https://docs.confluent.io/platform/current/connect/references/restapi.html)
- [Confluent Schema Registry](https://docs.confluent.io/platform/current/schema-registry/index.html)
- ADR 009 - `docs/adr/009-add-cdc-transactional-outbox-with-kafka.md`
