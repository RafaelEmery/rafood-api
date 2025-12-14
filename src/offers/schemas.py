from datetime import datetime, time
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from src.enums import Day


class OfferSchema(BaseModel):
	id: UUID
	product_id: UUID
	price: float
	active: bool
	created_at: datetime
	updated_at: datetime

	class Config:
		from_attributes = True


class OfferScheduleSchema(BaseModel):
	id: UUID
	offer_id: UUID
	day: Day
	start_time: time
	end_time: time
	repeats: bool
	created_at: datetime
	updated_at: datetime

	class Config:
		from_attributes = True
		json_encoders = {time: lambda v: v.strftime('%H:%M:%S')}


class OfferWithSchedulesSchema(OfferSchema):
	schedules: list[OfferScheduleSchema] = []


class CreateOfferSchema(BaseModel):
	product_id: UUID
	price: float = Field(gt=0)


class CreateOfferResponseSchema(BaseModel):
	id: UUID


class UpdateOfferSchema(BaseModel):
	price: float = Field(gt=0)
	active: bool


class CreateOfferScheduleSchema(BaseModel):
	day: Day
	start_time: str = Field(min_length=6, max_length=8)
	end_time: str = Field(min_length=6, max_length=8)
	repeats: bool

	@field_validator('start_time', 'end_time')
	@classmethod
	def validate_time_format(cls, v):
		"""Validate time format HH:MM:SS (00:00:00 to 23:59:59)"""
		try:
			parsed_time = datetime.strptime(v, '%H:%M:%S')

			if not (0 <= parsed_time.hour <= 23):
				raise ValueError('Hour must be between 00 and 23')

			return v
		except ValueError as e:
			raise ValueError('Time must be in HH:MM:SS format (00:00:00 to 23:59:59)') from e


class CreateOfferScheduleResponseSchema(BaseModel):
	id: UUID


class UpdateOfferScheduleSchema(CreateOfferScheduleSchema):
	pass
