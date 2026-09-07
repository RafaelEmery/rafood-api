# Confluent's Connect image already ships the Avro converter and the Kafka CLI tools,
# but it does not include Debezium. Kafka Connect only loads connectors found in
# CONNECT_PLUGIN_PATH, so the plugin has to be baked into the image.
FROM confluentinc/cp-kafka-connect:7.8.0

# Pinned on purpose: an unpinned "latest" would silently change the connector
# (and its Kafka/Java requirements) on every rebuild. The 2.5.x line runs on the
# JVM shipped with Confluent Platform 7.x.
ARG DEBEZIUM_POSTGRES_VERSION=2.5.4-3

# confluent-hub installs into /usr/share/confluent-hub-components, the second entry
# of CONNECT_PLUGIN_PATH in docker-compose.yml.
RUN confluent-hub install --no-prompt \
    debezium/debezium-connector-postgresql:${DEBEZIUM_POSTGRES_VERSION}
