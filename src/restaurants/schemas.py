from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl

from enums import Day, DayType


class RestaurantSchema(BaseModel):
	id: UUID
	name: str
	image_url: str
	owner_id: UUID
	street: str
	number: int
	neighborhood: str
	city: str
	state_abbr: str
	created_at: datetime
	updated_at: datetime

	class Config:
		from_attributes = True


class CreateRestaurantSchema(BaseModel):
	name: str = Field(max_length=256)
	image_url: str = HttpUrl
	owner_id: UUID
	street: str = Field(max_length=256)
	number: int = Field(ge=1)
	neighborhood: str = Field(max_length=256)
	city: str = Field(max_length=256)
	state_abbr: str = Field(max_length=2)


class CreateRestaurantResponseSchema(BaseModel):
	id: UUID


class UpdateRestaurantSchema(CreateRestaurantSchema):
	pass


# TODO: improve restaurant schedule schema
class RestaurantScheduleSchema(BaseModel):
	id: UUID


# TODO: validate if is one of Day or DayType Enums
class CreateRestaurantScheduleSchema(BaseModel):
	day_type: DayType | str = Field(max_length=10)
	start_day: Day | str = Field(max_length=10)
	end_day: Day | str = Field(max_length=10)
	start_time: str = Field(min_length=6, max_length=8)
	end_time: str = Field(min_length=6, max_length=8)


class CreateRestaurantScheduleResponseSchema(BaseModel):
	id: UUID


# TODO: validate if is one of Day or DayType Enums
class UpdateRestaurantScheduleSchema(BaseModel):
	day_type: DayType | str = Field(max_length=10)
	start_day: Day | str = Field(max_length=10)
	end_day: Day | str = Field(max_length=10)
	start_time: str = Field(min_length=6, max_length=8)
	end_time: str = Field(min_length=6, max_length=8)
