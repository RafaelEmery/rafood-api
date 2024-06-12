from uuid import UUID
from datetime import datetime
from typing import List

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


# TODO: set parameters to nullable at UpdateRestaurantSchema
class UpdateRestaurantSchema(CreateRestaurantSchema):
	pass


# TODO: improve restaurant schedule schema
class RestaurantScheduleSchema(BaseModel):
	id: UUID


# TODO: improve validation for creating schedule
class CreateRestaurantScheduleSchema(BaseModel):
	restaurant_id: UUID
	day_type: List[DayType]
	start_day: List[Day]
	end_day: List[Day]
	start_time: str = Field(max_length=6)
	end_time: str = Field(max_length=6)


class CreateRestaurantScheduleResponseSchema(BaseModel):
	id: UUID


class UpdateRestaurantScheduleSchema(BaseModel):
	day_type: List[DayType]
	start_day: List[Day]
	end_day: List[Day]
	start_time: str = Field(max_length=6)
	end_time: str = Field(max_length=6)
