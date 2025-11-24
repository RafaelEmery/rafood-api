from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel


class Product(SQLModel, table=True):
	__tablename__ = 'products'

	id: UUID = Field(default_factory=uuid4, primary_key=True)
	restaurant_id: UUID = Field(foreign_key='restaurants.id')
	name: str = Field(max_length=256)
	price: float
	category_id: UUID = Field(foreign_key='categories.id')
	image_url: str | None = Field(default=None, max_length=256)
	created_at: datetime = Field(default_factory=datetime.now)
	updated_at: datetime = Field(
		default_factory=datetime.now, sa_column_kwargs={'onupdate': datetime.now}
	)

	restaurant: Optional['Restaurant'] = Relationship(back_populates='products')  # noqa: F821
	category: Optional['Category'] = Relationship(  # noqa: F821
		back_populates='products', sa_relationship_kwargs={'lazy': 'joined'}
	)
	offers: list['Offer'] = Relationship(  # noqa: F821
		back_populates='product', sa_relationship_kwargs={'lazy': 'joined'}
	)
