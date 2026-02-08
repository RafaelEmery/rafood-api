# mypy: disable-error-code=name-defined
from datetime import datetime, time
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel


class Offer(SQLModel, table=True):
	__tablename__ = 'offers'

	id: UUID = Field(default_factory=uuid4, primary_key=True)
	product_id: UUID = Field(foreign_key='products.id')
	price: float
	active: bool = Field(default=True)
	created_at: datetime = Field(default_factory=datetime.now)
	updated_at: datetime = Field(
		default_factory=datetime.now, sa_column_kwargs={'onupdate': datetime.now}
	)

	product: Optional['Product'] = Relationship(back_populates='offers')  # noqa: F821
	schedules: list['OfferSchedule'] = Relationship(
		back_populates='offer', sa_relationship_kwargs={'lazy': 'joined'}
	)


class OfferSchedule(SQLModel, table=True):
	__tablename__ = 'offer_schedules'

	id: UUID = Field(default_factory=uuid4, primary_key=True)
	offer_id: UUID = Field(foreign_key='offers.id')
	day: str = Field(max_length=10)
	start_time: time
	end_time: time
	repeats: bool = Field(default=False)
	created_at: datetime = Field(default_factory=datetime.now)
	updated_at: datetime = Field(
		default_factory=datetime.now, sa_column_kwargs={'onupdate': datetime.now}
	)

	offer: Optional['Offer'] = Relationship(back_populates='schedules')
