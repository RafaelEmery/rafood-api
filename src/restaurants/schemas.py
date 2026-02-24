from datetime import datetime, time
from uuid import UUID

from pydantic import BaseModel, Field, HttpUrl, field_validator

from src.enums import Day, DayType
from src.products.schemas import ProductSchema


class RestaurantSchema(BaseModel):
	id: UUID
	name: str
	image_url: str | None
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


class RestaurantScheduleSchema(BaseModel):
	id: UUID
	day_type: str
	start_day: str
	end_day: str
	start_time: time
	end_time: time
	created_at: datetime
	updated_at: datetime

	class Config:
		from_attributes = True
		json_encoders = {time: lambda v: v.strftime('%H:%M:%S')}


class RestaurantWithSchedulesSchema(RestaurantSchema):
	schedules: list[RestaurantScheduleSchema] = []


class RestaurantWithProductsSchema(RestaurantSchema):
	products: list[ProductSchema] = []


class CreateRestaurantSchema(BaseModel):
	name: str = Field(min_length=1, max_length=256)
	image_url: HttpUrl | None = None
	owner_id: UUID
	street: str = Field(min_length=1, max_length=256)
	number: int = Field(ge=1)
	neighborhood: str = Field(min_length=1, max_length=256)
	city: str = Field(min_length=1, max_length=256)
	state_abbr: str = Field(min_length=2, max_length=2)

	@field_validator('image_url')
	@classmethod
	def convert_url_to_string(cls, v: HttpUrl | None) -> str | None:
		"""Convert HttpUrl to string for database storage"""
		if v is not None:
			return str(v)
		return v


class CreateRestaurantResponseSchema(BaseModel):
	id: UUID


class UpdateRestaurantSchema(CreateRestaurantSchema):
	pass


class CreateRestaurantScheduleSchema(BaseModel):
	day_type: DayType
	start_day: Day
	end_day: Day
	start_time: str
	end_time: str

	@field_validator('start_time', 'end_time')
	@classmethod
	def validate_time_format(cls, v: str) -> str:
		"""Validate time format HH:MM:SS (00:00:00 to 23:59:59)"""
		try:
			parsed_time = datetime.strptime(v, '%H:%M:%S')

			if not (0 <= parsed_time.hour <= 23):
				raise ValueError('Hour must be between 00 and 23')

			return v
		except ValueError as e:
			raise ValueError('Time must be in HH:MM:SS format (00:00:00 to 23:59:59)') from e


class CreateRestaurantScheduleResponseSchema(BaseModel):
	id: UUID


class UpdateRestaurantScheduleSchema(CreateRestaurantScheduleSchema):
	pass
