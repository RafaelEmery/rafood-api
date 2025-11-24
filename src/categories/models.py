from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel


class Category(SQLModel, table=True):
	__tablename__ = 'categories'

	id: UUID = Field(default_factory=uuid4, primary_key=True)
	name: str = Field(max_length=256)
	created_at: datetime = Field(default_factory=datetime.now)
	updated_at: datetime = Field(
		default_factory=datetime.now, sa_column_kwargs={'onupdate': datetime.now}
	)

	products: list['Product'] = Relationship(back_populates='category')  # noqa: F821
