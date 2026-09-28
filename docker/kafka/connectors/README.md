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

- `outbox.event.product.created`
- `outbox.event.product.updated`
- `outbox.event.product.deleted`

The API writes only product events today. A later aggregate is added to `TOPICS` in `../setup.sh` when that domain starts writing the outbox. The sink already matches `outbox.event.*`.

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

**Ordering across event types is not guaranteed.** Kafka orders messages per partition, and there is no ordering between topics. A consumer can see `product.deleted` before the `product.updated` that came first in the database. Order per product is preserved *within* each topic thanks to the key.

The Elasticsearch sink deletes the document when the topic ends in `.deleted`. It does not compare `updated_at`, so a later `updated` on the other topic can upsert that document back. Routing all types to a single topic (`route.by.field=aggregatetype`) is the alternative that restores total order per product.

**Replication factor is 1.** The profile runs a single broker, and the replication factor can never exceed the broker count. There is no replica durability: if the broker loses its volume, the events are gone. To move to RF 3, add two more brokers to the `kafka` service definition (distinct `KAFKA_NODE_ID` and controller quorum voters), then raise `REPLICATION_FACTOR` in `../setup.sh`, `topic.creation.default.replication.factor` here, and the `*_REPLICATION_FACTOR` variables of Kafka, Connect, Schema Registry and Control Center in `docker/docker-compose.yml`.

**`wal_level=logical` needs a Postgres restart.** It is set as a `command` flag on the `database` service. An already running container keeps the old value until it is recreated (`docker compose -f docker/docker-compose.yml up -d database`); the data volume is not affected.

## Verifying

```bash
# Connector state and tasks
curl -s localhost:8083/connectors/rafood-outbox-connector/status | jq

# Registered Avro schemas
curl -s localhost:8081/subjects

# Read the events (from inside the broker container)
docker compose -f docker/docker-compose.yml exec kafka kafka-console-consumer \
  --bootstrap-server kafka:29092 \
  --topic outbox.event.product.created \
  --from-beginning --property print.key=true
```

For the Avro value in a readable form, use `kafka-avro-console-consumer` from the Schema Registry container:

```bash
docker compose -f docker/docker-compose.yml exec schema-registry kafka-avro-console-consumer \
  --bootstrap-server kafka:29092 \
  --property schema.registry.url=http://schema-registry:8081 \
  --topic outbox.event.product.created --from-beginning
```

Control Center (topics, throughput, connector status) runs at `http://localhost:9021`.

## Elasticsearch sink connector

`elastic-search-sink-connector.json` is registered by `../setup.sh` as `rafood-elasticsearch-sink`. Connect names the consumer group `connect-rafood-elasticsearch-sink` from that connector name. The file is the config object only, sent with `PUT /connectors/rafood-elasticsearch-sink/config`.

```text
outbox.event.<aggregate>.<action>
  -> Drop$Value on topics ending in .deleted (value becomes null; the Kafka record is unchanged)
  -> RegexRouter rewrites the topic to <aggregate>, which is the index name
  -> upsert the document id (the message key), or delete it when the value is null
```

Created and updated overwrite one document per aggregate id in the index named after the aggregate (`product` today). A topic ending in `.deleted` removes that document, so search no longer returns it. The event on Kafka stays the full snapshot; only this sink sees a tombstone.

Drop runs before RegexRouter. After the rename the topic is only `product`, and the delete predicate would not match.

### Properties

| Property                                            | Why it matters                                                                                                                                                                          |
| --------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `connector.class`                                   | Elasticsearch sink installed in the Connect image (`kafka-connect-elasticsearch` 14.1.0).                                                                                               |
| `topics.regex=outbox\.event\..*`                    | Every outbox topic, including ones added later, without listing them here.                                                                                                              |
| `connection.url=http://elasticsearch:9200`          | Compose service name. Security is off on that service, so there is no username.                                                                                                         |
| `key.ignore=false`                                  | Document id is the Kafka key (`aggregateid`). Created, updated, and deleted hit the same id.                                                                                            |
| `schema.ignore=true`                                | Elasticsearch infers the mapping from the document instead of the Connect schema.                                                                                                       |
| `write.method=upsert`                               | A repeated id overwrites the document. Created and updated share one document.                                                                                                          |
| `behavior.on.null.values=delete`                    | A null value deletes the document for that key. The default `fail` would stop the task on a delete event.                                                                               |
| `predicates.isDelete` + `Drop$Value`                | Topics matching `outbox.event.<aggregate>.deleted` have their value set to null before the sink writes. Other topics are unchanged. `Drop$Value` comes from `connect-transforms` 1.6.2. |
| `transforms.indexName` (RegexRouter)                | Index name is the aggregate (`$1` in `outbox.event.<aggregate>.<action>`), not the full topic.                                                                                          |
| `errors.log.enable` / `errors.log.include.messages` | Failed records are logged with their content (`make logs container=connect`).                                                                                                           |

Worker-level Avro conversion is reused (`CONNECT_VALUE_CONVERTER` and the Schema Registry URL). This file does not set converters.

### Verifying

```bash
curl -s localhost:8083/connectors/rafood-elasticsearch-sink/status | jq
curl -s localhost:9200/product/_doc/<uuid>
curl -s 'localhost:9200/product/_search?q=hamburguer'
```

After a product delete, `/product/_doc/<uuid>` is `found: false` and the search no longer returns it. A later aggregate is indexed the same way once its topics exist and the outbox writes them.

## References

- [Debezium Outbox Event Router](https://debezium.io/documentation/reference/stable/transformations/outbox-event-router.html)
- [Debezium connector for PostgreSQL](https://debezium.io/documentation/reference/stable/connectors/postgresql.html)
- [Kafka Connect REST API](https://docs.confluent.io/platform/current/connect/references/restapi.html)
- [Confluent Schema Registry](https://docs.confluent.io/platform/current/schema-registry/index.html)
- [Confluent Elasticsearch Sink](https://docs.confluent.io/kafka-connect-elasticsearch/current/)
- [Drop SMT](https://docs.confluent.io/kafka-connectors/transforms/current/drop.html)
- ADR 009 - `docs/adr/009-add-cdc-transactional-outbox-with-kafka.md`
