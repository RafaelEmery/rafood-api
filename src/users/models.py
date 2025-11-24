from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
	__tablename__ = 'users'

	id: UUID = Field(default_factory=uuid4, primary_key=True)
	first_name: str = Field(max_length=256)
	last_name: str = Field(max_length=256)
	email: str = Field(max_length=256)
	password: str = Field(max_length=256)
	created_at: datetime = Field(default_factory=datetime.now)
	updated_at: datetime = Field(
		default_factory=datetime.now, sa_column_kwargs={'onupdate': datetime.now}
	)

	# Relationships
	restaurants: list['Restaurant'] = Relationship(  # noqa: F821
		back_populates='owner', sa_relationship_kwargs={'lazy': 'joined'}
	)
