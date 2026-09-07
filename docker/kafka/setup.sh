#!/usr/bin/env bash
# One-shot setup for the "kafka" Compose profile: creates the product event topics
# and registers the Debezium outbox connector. Runs on every `up` and is safe to
# repeat, so there is no Makefile target for it.
set -euo pipefail

BOOTSTRAP_SERVER="kafka:29092"
CONNECT_URL="http://connect:8083"
CONNECTOR_NAME="rafood-outbox-connector"
CONNECTOR_TEMPLATE="/setup/connectors/outbox-source.json"
RENDERED_CONNECTOR="/tmp/outbox-source.rendered.json"

# One topic per outbox `type` value, matching transforms.outbox.route.by.field=type.
TOPICS=(
  "outbox.event.ProductCreated"
  "outbox.event.ProductUpdated"
  "outbox.event.ProductDeleted"
)

# More than one partition (parallel consumers later); ordering per product is kept
# by the message key, not by having a single partition.
PARTITIONS=3
# Single broker in this profile, so 1 is the only valid replication factor.
REPLICATION_FACTOR=1

wait_for_kafka() {
  echo "Waiting for Kafka at ${BOOTSTRAP_SERVER}..."
  # The Compose healthcheck already gates this container, but the loop keeps the
  # script usable on its own (docker compose run kafka-setup).
  until kafka-broker-api-versions --bootstrap-server "${BOOTSTRAP_SERVER}" >/dev/null 2>&1; do
    sleep 2
  done
}

create_topics() {
  for topic in "${TOPICS[@]}"; do
    # --if-not-exists keeps re-runs idempotent instead of failing on the second `up`.
    kafka-topics \
      --bootstrap-server "${BOOTSTRAP_SERVER}" \
      --create --if-not-exists \
      --topic "${topic}" \
      --partitions "${PARTITIONS}" \
      --replication-factor "${REPLICATION_FACTOR}" \
      --config cleanup.policy=delete
    echo "Topic ready: ${topic}"
  done
}

wait_for_connect() {
  echo "Waiting for Kafka Connect at ${CONNECT_URL}..."
  until curl -fsS "${CONNECT_URL}/connectors" >/dev/null 2>&1; do
    sleep 2
  done
}

render_connector_config() {
  # Credentials stay out of the committed JSON; Compose passes them as env vars.
  sed \
    -e "s|__DB_USER__|${DB_USER}|" \
    -e "s|__DB_PASSWORD__|${DB_PASSWORD}|" \
    -e "s|__DB_NAME__|${DB_NAME}|" \
    "${CONNECTOR_TEMPLATE}" >"${RENDERED_CONNECTOR}"
}

register_connector() {
  # PUT on /config creates or updates the connector; POST /connectors would return
  # 409 Conflict once it already exists.
  curl -fsS -X PUT \
    -H "Content-Type: application/json" \
    --data "@${RENDERED_CONNECTOR}" \
    "${CONNECT_URL}/connectors/${CONNECTOR_NAME}/config" >/dev/null
  echo "Connector ready: ${CONNECTOR_NAME}"
}

wait_for_kafka
create_topics
wait_for_connect
render_connector_config
register_connector

echo "Kafka CDC setup finished."
