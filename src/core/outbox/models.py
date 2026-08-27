from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel


class OutboxEvent(SQLModel, table=True):
	"""
	Durable outbox row written in the same transaction as a domain change.

	The API does not publish to Kafka directly; CDC (Debezium) reads inserts
	from this table and routes them to topics. Column names follow the default
	Debezium Outbox Event Router contract.

	Columns:
	- id: unique event id (dedup / tracing).
	- aggregatetype: aggregate family for topic routing (outbox.event.${aggregatetype}).
	- aggregateid: aggregate instance id; typically the Kafka message key.
	- type: domain event name used by consumers to dispatch.
	- payload: event body (JSONB snapshot consumers need).

	Consumers typically use aggregatetype for the topic, aggregateid as key,
	type (and id) in headers for routing/idempotency, and payload as the body.

	External references:
	- https://microservices.io/patterns/data/transactional-outbox.html
	- https://debezium.io/documentation/reference/stable/transformations/outbox-event-router.html
	"""

	__tablename__ = 'outbox'

	id: UUID = Field(
		default_factory=uuid4,
		primary_key=True,
		description='Unique event id for tracing and consumer deduplication.',
	)
	aggregatetype: str = Field(
		max_length=255,
		description='Aggregate family used by Debezium to route the Kafka topic.',
	)
	aggregateid: str = Field(
		max_length=255,
		description='Aggregate instance id; typically the Kafka message key.',
	)
	type: str = Field(
		max_length=255,
		description='Domain event name used by consumers to dispatch handling.',
	)
	payload: dict[str, Any] | None = Field(
		default=None,
		sa_column=Column(JSONB, nullable=True),
		description='Event body snapshot consumed after CDC publishes to Kafka.',
	)
