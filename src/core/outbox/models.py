from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel


class OutboxEvent(SQLModel, table=True):
	__tablename__ = 'outbox'

	id: UUID = Field(default_factory=uuid4, primary_key=True)
	aggregatetype: str = Field(max_length=255)
	aggregateid: str = Field(max_length=255)
	type: str = Field(max_length=255)
	payload: dict[str, Any] | None = Field(
		default=None,
		sa_column=Column(JSONB, nullable=True),
	)
