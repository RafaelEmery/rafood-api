# mypy: disable-error-code=name-defined
from datetime import datetime, time
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel


class Restaurant(SQLModel, table=True):
	__tablename__ = 'restaurants'

	id: UUID = Field(default_factory=uuid4, primary_key=True)
	name: str = Field(max_length=256)
	image_url: str | None = Field(default=None, max_length=256)
	owner_id: UUID = Field(foreign_key='users.id')
	street: str = Field(max_length=256)
	number: int
	neighborhood: str = Field(max_length=256)
	city: str = Field(max_length=256)
	state_abbr: str = Field(max_length=2)
	created_at: datetime = Field(default_factory=datetime.now)
	updated_at: datetime = Field(
		default_factory=datetime.now, sa_column_kwargs={'onupdate': datetime.now}
	)

	owner: Optional['User'] = Relationship(back_populates='restaurants')  # noqa: F821
	products: list['Product'] = Relationship(  # noqa: F821
		back_populates='restaurant', sa_relationship_kwargs={'lazy': 'joined'}
	)
	schedules: list['RestaurantSchedule'] = Relationship(
		back_populates='restaurant', sa_relationship_kwargs={'lazy': 'joined'}
	)


class RestaurantSchedule(SQLModel, table=True):
	__tablename__ = 'restaurant_schedules'

	id: UUID = Field(default_factory=uuid4, primary_key=True)
	restaurant_id: UUID = Field(foreign_key='restaurants.id')
	day_type: str = Field(max_length=10)
	start_day: str = Field(max_length=10)
	end_day: str = Field(max_length=10)
	start_time: time
	end_time: time
	created_at: datetime = Field(default_factory=datetime.now)
	updated_at: datetime = Field(
		default_factory=datetime.now, sa_column_kwargs={'onupdate': datetime.now}
	)

	restaurant: Optional['Restaurant'] = Relationship(back_populates='schedules')
