# Confluent's Connect image already ships the Avro converter and the Kafka CLI tools,
# but it does not include Debezium, the Elasticsearch sink, or the Drop SMT.
# Kafka Connect only loads plugins found in CONNECT_PLUGIN_PATH, so they have to
# be baked into the image.
FROM confluentinc/cp-kafka-connect:7.8.0

# Pinned on purpose: an unpinned "latest" would silently change the plugin
# (and its Kafka/Java requirements) on every rebuild.
# Debezium 2.5.x runs on the JVM shipped with Confluent Platform 7.x.
# connect-transforms 1.6.2 supplies Drop$Value, which the base image does not ship.
ARG DEBEZIUM_POSTGRES_VERSION=2.5.4-3
ARG ELASTICSEARCH_SINK_VERSION=14.1.0
ARG CONNECT_TRANSFORMS_VERSION=1.6.2

# confluent-hub installs into /usr/share/confluent-hub-components, the second entry
# of CONNECT_PLUGIN_PATH in docker/docker-compose.yml.
RUN confluent-hub install --no-prompt \
    debezium/debezium-connector-postgresql:${DEBEZIUM_POSTGRES_VERSION} \
 && confluent-hub install --no-prompt \
    confluentinc/kafka-connect-elasticsearch:${ELASTICSEARCH_SINK_VERSION} \
 && confluent-hub install --no-prompt \
    confluentinc/connect-transforms:${CONNECT_TRANSFORMS_VERSION}
