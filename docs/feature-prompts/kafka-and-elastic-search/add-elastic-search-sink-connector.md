@.cursor/prompts/feature-agent.md

## Context

Add a new Elastic Search sink connector to the Kafka Connectors. The connector should be able to read events from the Kafka topics and write them to the Elastic Search index.

> Add a new markdown file to the plans folter (you can create the folder if it doesn't exist), containing the plan related to this feature prompt

## Logic flow

> The example is based on the product created event but must be applied to all other outbox events.

- Product is created in the database.
- Product is published to the Kafka topic.
- The Kafka Connect connector reads the event from the Kafka topic.
- The connector writes the event to the Elastic Search index.
- The connector has a consumer group that reads the events from the Kafka topics and writes them to the Elastic Search index.
- Has products in the Elastic Search index.

## Acceptance criteria

- The connector is added to the Kafka Connectors.
- The connector is able to read events from the Kafka topics and write them to the Elastic Search index.

## Extra

### Elastic Search configuration example

On `docker-compose.yml` file, you can see the Elastic Search configuration example:

```yaml
elasticsearch:
  image: docker.elastic.co/elasticsearch/elasticsearch:8.15.3
  container_name: rafood_elasticsearch
  profiles: ["kafka"]
  environment:
    discovery.type: single-node
    xpack.security.enabled: "false"
    xpack.security.enrollment.enabled: "false"
    xpack.security.http.ssl.enabled: "false"
    xpack.security.transport.ssl.enabled: "false"
    ES_JAVA_OPTS: "-Xms512m -Xmx512m"
  ports:
    - "9200:9200"
  volumes:
    - elasticsearch_data:/usr/share/elasticsearch/data
  healthcheck:
    test: ["CMD-SHELL", "curl -fsS http://localhost:9200 >/dev/null || exit 1"]
    interval: 10s
    timeout: 5s
    retries: 20
    start_period: 40s
```

### Elastic Search sink connector example

On `docker/kafka/connectors/elastic-search-sink-connector.json` file, you can see the Elastic Search sink connector example:

```json
{
  "connector.class": "io.confluent.connect.elasticsearch.ElasticsearchSinkConnector",
  "tasks.max": "1",
  "topics.regex": "outbox\\.event\\..*",
  "connection.url": "http://elasticsearch:9200",
  "key.ignore": "false",
  "schema.ignore": "true",
  "write.method": "upsert",
  "transforms": "indexName",
  "transforms.indexName.type": "org.apache.kafka.connect.transforms.RegexRouter",
  "transforms.indexName.regex": "outbox\\.event\\.([^.]+)\\..*",
  "transforms.indexName.replacement": "$1",
  "errors.log.enable": "true",
  "errors.log.include.messages": "true"
}
```

### Elastic Search volume example

On `docker/docker-compose.yml` file, in the `volumes` block, you can see the Elastic Search volume example:

```yaml
elasticsearch_data:
```

### Kafka setup depends on Elastic Search example

On `docker/docker-compose.yml` file, in `kafka-setup.depends_on`, you can see the Elastic Search dependency example:

```yaml
elasticsearch:
  condition: service_healthy
```

### Elastic Search sink plugin example

On `docker/kafka-connect/Dockerfile` file, you can see the Elastic Search sink plugin example:

```dockerfile
ARG ELASTICSEARCH_SINK_VERSION=14.1.0

RUN confluent-hub install --no-prompt \
    confluentinc/kafka-connect-elasticsearch:${ELASTICSEARCH_SINK_VERSION}
```

### Elastic Search sink registration example

On `docker/kafka/setup.sh` file, you can see the Elastic Search sink registration example. The connector name becomes the consumer group `connect-rafood-elasticsearch-sink`.

```bash
ES_URL="http://elasticsearch:9200"
ES_CONNECTOR_NAME="rafood-elasticsearch-sink"
ES_CONNECTOR_CONFIG="/setup/connectors/elastic-search-sink-connector.json"

wait_for_elasticsearch() {
  echo "Waiting for Elasticsearch at ${ES_URL}..."
  until curl -fsS "${ES_URL}" >/dev/null 2>&1; do
    sleep 2
  done
}

register_elasticsearch_sink() {
  curl -fsS -X PUT \
    -H "Content-Type: application/json" \
    --data "@${ES_CONNECTOR_CONFIG}" \
    "${CONNECT_URL}/connectors/${ES_CONNECTOR_NAME}/config" >/dev/null
  echo "Connector ready: ${ES_CONNECTOR_NAME}"
}
```

```bash
wait_for_elasticsearch
register_elasticsearch_sink
```

### Verification example

```bash
make start-kafka
curl -s localhost:8083/connectors/rafood-elasticsearch-sink/status
curl -s localhost:9200/product/_doc/<uuid>
curl -s 'localhost:9200/product/_search?q=hamburguer'
```

`topics.regex` is `outbox.event.*`, so a later aggregate is indexed once its topics are added to `TOPICS` in `docker/kafka/setup.sh` and that domain writes the outbox. Do not pre-create those topics.

## References

- [ADR 009](../../adr/009-add-cdc-transactional-outbox-with-kafka.md)
- [Kafka Guide](../../kafka-events-guide.md)
