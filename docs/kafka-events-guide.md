# Events Architecture Guide (Kafka)

Configurations, usage and other details will be updated as the project progresses.

## TL;DR

- Produce events by creating on `public.outbox` table.
- Debezium watches the outbox table after commit and publishes each event to a Kafka topic.
- Schema Registry (Avro) describes the message payload so consumers can read a stable schema.
- Elasticsearch sink reads `outbox.event.*` and indexes the events.

```bash
make start-kafka
```

> If `outbox` table hasn\`t been created yet, you need to apply migrations first.

```bash
make migrate
```

Access Control Center at `http://localhost:9021` and see the topics and their partitions, Kafka Connect, consumers, replicators, and others.

Call any API to produce events on the topics.

To remove, stop or restart containers:

```bash
make down-kafka
make stop-kafka
make restart-kafka
```

## Overview

### Transactional Outbox Pattern with Unit of Work pattern

Domain changes and their events are written in the same database transaction via the Unit of Work, so a rollback never leaves a half-published event. The API only persists the aggregate and an outbox row; it never produces to Kafka. This is currently used for the product domain.

### CDC (Change Data Capture) with Debezium and Kafka

Debezium watches the outbox table after commit and publishes each event to a Kafka topic. Schema Registry (Avro) describes the message payload so consumers can read a stable schema.

## Local Setup and Configuration

### Setup

Migrations must be applied to the database before running the application.

```bash
make migrate
```

Start containers with `kafka` profile:

```bash
make start-kafka
```

### The outbox table

`public.outbox` is written in the same transaction as the domain change. Columns follow the Debezium Outbox Event Router contract: `id`, `aggregatetype` (today `product`), `aggregateid` (Kafka key), `type` (`product.created`, `product.updated`, `product.deleted`), and `payload` (JSONB snapshot of `ProductSchema`).

Field notes are on `OutboxEvent` in `src/core/outbox/models.py`.

### Debezium connector configuration

`docker/kafka/connectors/outbox-source.json` is applied by `kafka-setup` as `rafood-outbox-connector`. It reads only `public.outbox` through `pgoutput` (slot `debezium_outbox`). The EventRouter expands the JSON payload, routes on `type` to `outbox.event.${type}`, and sets the key from `aggregateid` (`eventType` is a header).

Each property is documented in `docker/kafka/connectors/README.md`.

### Kafka configuration

One KRaft broker (no ZooKeeper): containers use `kafka:29092`, the host uses `localhost` on `KAFKA_PORT` (default 9092). Replication factor is 1 and `auto.create.topics.enable` is false, so `kafka-setup` creates the product topics (3 partitions, `cleanup.policy=delete`). The API writes only product events. A new aggregate's topics go in `TOPICS` in `docker/kafka/setup.sh` when that domain starts writing the outbox.

The commented broker settings are on the `kafka` service in `docker/docker-compose.yml`.

### Schema registry configuration

There is no `.avsc` in the repo. The connector value is Avro (`AvroConverter` → `http://schema-registry:8081`); Connect infers the schema from the expanded outbox JSON and auto-registers it (default BACKWARD). The API only writes `ProductSchema` into the outbox — Connect is the producer, the Registry just versions what it gets.

### Elastic Search sink connector

The `kafka` profile runs Elasticsearch 8.15 at `http://localhost:9200` (security off). `kafka-setup` registers the sink connector `rafood-elasticsearch-sink` (consumer group `connect-rafood-elasticsearch-sink`), which reads `outbox.event.*`.

The index is the aggregate (`product` today) and the document id is the aggregate id: created and updated upsert it; a topic ending in `.deleted` removes it, while the Kafka event stays the full snapshot. RegexRouter turns `outbox.event.<aggregate>.<action>` into that index. `flush.synchronously=true` is what allows the rename on connector 14.1.0. Those topics are not ordered against each other, so a later update can write the document again.

Each property and how to verify are documented in `docker/kafka/connectors/README.md`.

## Usage

### Producing Outbox Events

> Currently it's only implemented for product domain.

Create/update or delete a product:

```bash
curl -sS -X POST 'http://localhost:8000/api/v1/products' \
  -H 'Content-Type: application/json' \
  -d '{
    "restaurant_id": "6e13f353-4f9e-4e22-b11c-2ba668fda528",
    "name": "Hambúrguer artesanal",
    "price": 29.99,
    "category_id": "095e1c0f-dec1-42cd-83c1-4a8cc6bd488a",
    "image_url": "https://example.com/product.jpg"
  }'
```

At the same unit of work, the product will be created/updated or deleted and the outbox event will be produced (created at `outbox` table).

The outbox table will be updated with the event data:

> [!NOTE]
> At the screenshot below, you can see the `outbox.type` column on PascalCase format but was refactored to `model.action` on lower case (e.g. `product.created`, `product.updated`, `product.deleted`).

![Product Outbox Events Postgres](./images/product-outbox-events-postgres.png)

### Nagivate on Control Center

Access Control Center at `http://localhost:9021`

![Control Center initial screen](./images/kafka-control-center-first.png)

You can see the topics and their partitions, Kafka Connect, consumers, replicators, and others.

Topics screen:

![Control Center topics screen](./images/kafka-control-center-topics.png)

### Events on topics

Go to messages screen to see the events on topics:

![Control Center messages screen](./images/kafka-control-center-topics-message.png)

Example of message header on `outbox.event.product.created` topic:

```json
[
  {
    "key": "id",
    "value": "5449ba94-b5bc-420c-8d9f-2a10e651cdfb"
  },
  {
    "key": "eventType",
    "value": "product.created"
  }
]
```

Example of message payload on `outbox.event.product.created` topic:

```json
{
  "payload": {
    "id": {
      "string": "92546e50-d33f-4bcd-9572-054ce596e6a6"
    },
    "name": {
      "string": "Licensed Cotton Cheese"
    },
    "price": {
      "double": 12.3
    },
    "image_url": {
      "string": "http://placeimg.com/640/480"
    },
    "created_at": {
      "string": "2026-09-13T18:35:14.955897"
    },
    "updated_at": {
      "string": "2026-09-13T18:35:14.955902"
    },
    "category_id": {
      "string": "3ddd3703-6331-4a79-8af1-04bac779c519"
    },
    "restaurant_id": {
      "string": "2f8f4eb2-2202-4e31-a537-1c3f9706abf4"
    }
  }
}
```

You can check the Schema Registry for the message payload, it's versions, types and even evolve schema if needed.

![Schema Registry screen](./images/kafka-control-center-schema-registry.png)

### To improve message payload and/or Schema Registry

You can improve the message payload and/or Schema Registry by adding a new column to the outbox table and updating the schema registry.

### Add new topics (example: restaurant)

The topic name is the outbox `type`: `restaurant.created` is published to `outbox.event.restaurant.created`. The connector JSON and the outbox table stay as they are (`route.by.field=type`).

- Write the row in the same transaction as the restaurant change: `aggregatetype=restaurant`, `aggregateid` = the restaurant id, `type=restaurant.created`, `restaurant.updated`, or `restaurant.deleted`, `payload` = the restaurant snapshot. Follow `src/products/outbox_events.py` and the product service. The restaurants repository still commits on its own, so that commit has to move to the service `UnitOfWork`, or the outbox row is not in the same transaction.
- Add `outbox.event.restaurant.created`, `updated`, and `deleted` to `TOPICS` in `docker/kafka/setup.sh`. They are not created until then.
- Run `make restart-kafka` so `kafka-setup` creates those topics. Schema Registry registers the new payload on the first event; there is no `.avsc` to add. The Elasticsearch sink already matches `outbox.event.*`, and RegexRouter names the index after the aggregate (`restaurant`). A plugin change still needs `make start-kafka`, which rebuilds Connect.

### Kafka events upsert on Elastic Search indexes

After `make start-kafka` for creating the Kafka/Debezium/Elastic Search setup. If sink connector setup is ok, you'll see at Control Center and `Connect` screen:

![Kafka Control Center Sink Connector](./images/kafka-control-center-sink-connector.png)

Create a new product:

```bash
curl --location 'localhost:8000/api/v1/products' \
--header 'Content-Type: application/json' \
--data '{
    "restaurant_id": "2f8f4eb2-2202-4e31-a537-1c3f9706abf4",
    "name": "Esfirra de carne",
    "price": 12.3,
    "category_id": "3ddd3703-6331-4a79-8af1-04bac779c519",
    "image_url": "http://placeimg.com/640/480"
}'
```

The consumer group is named `connect-rafood-elasticsearch-sink` and you can see the consumption info at Control Center and `Consumer Groups` screen:

![Kafka Control Center Sink Consumer Group Lag](./images/kafka-control-center-sink-consumer-group-lag.png)

Topics, partitions and offsets:

![Kafka Control Center Sink Consumer Group Offsets](./images/kafka-control-center-sink-consumer-group-offsets.png)

> [!IMPORTANT]
> The topic names follow the `outbox.event.<aggregate>.<action>` pattern. The indexes follow the aggregate name. So all product topics are mapped to the `product` index. For other topics and indexes, the logic is to use the aggregate name as the index name.
> The `delete` action marks the document as deleted and the full snapshot is kept in the topic.

To validate the Elastic Search index and do a full text search, you can use the `curl` command:

```bash
curl -s 'localhost:9200/product/_search?q=Esfirra&pretty'
```

Pretty response:

![Elastic Search basic index query](./images/elastic-search-basic-index-query.png)

> [!NOTE]
> The current example uses the Elastic Search REST API but Kibana (using Docker Compose) can be integrated on the future.

<details>
<summary>Other Elastic Search indexes query examples for this product</summary>

```bash
curl -s 'localhost:9200/product/_search?pretty' -H 'Content-Type: application/json' -d '{"query":{"match":{"name":"esfirra"}}}'
```

```bash
curl -s 'localhost:9200/product/_search?pretty' -H 'Content-Type: application/json' -d '{"query":{"match":{"name":"ESFIRRA"}}}'
```

```bash
curl -s 'localhost:9200/product/_search?pretty' -H 'Content-Type: application/json' -d '{"query":{"match":{"name":"carne"}}}'
```

```bash
curl -s 'localhost:9200/product/_search?pretty' -H 'Content-Type: application/json' -d '{"query":{"match_phrase":{"name":"esfirra de carne"}}}'
```

```bash
curl -s 'localhost:9200/product/_search?pretty' -H 'Content-Type: application/json' -d '{"query":{"match":{"name":{"query":"esfirra carne","operator":"and"}}}}'
```

```bash
curl -s 'localhost:9200/product/_search?pretty' -H 'Content-Type: application/json' -d '{"query":{"query_string":{"query":"esfirra AND carne","default_field":"name"}}}'
```

```bash
curl -s 'localhost:9200/product/_search?pretty' -H 'Content-Type: application/json' -d '{"query":{"multi_match":{"query":"esfirra","fields":["name"]}}}'
```

```bash
curl -s 'localhost:9200/product/_search?pretty' -H 'Content-Type: application/json' -d '{"query":{"match":{"name":{"query":"esfira","fuzziness":"AUTO"}}}}'
```

```bash
curl -s 'localhost:9200/product/_search?pretty' -H 'Content-Type: application/json' -d '{"query":{"match":{"name":{"query":"esfirraa","fuzziness":"AUTO"}}}}'
```

```bash
curl -s 'localhost:9200/product/_search?pretty' -H 'Content-Type: application/json' -d '{"query":{"match":{"name":{"query":"esfírrá","fuzziness":"AUTO"}}}}'
```

```bash
curl -s 'localhost:9200/product/_search?pretty' -H 'Content-Type: application/json' -d '{"query":{"prefix":{"name":"esf"}}}'
```

```bash
curl -s 'localhost:9200/product/_search?pretty' -H 'Content-Type: application/json' -d '{"query":{"wildcard":{"name":"*sfirra*"}}}'
```

</details>
