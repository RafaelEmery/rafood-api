from datetime import datetime, time
from uuid import UUID

from pydantic import BaseModel, Field

from src.enums import Day


class OfferSchema(BaseModel):
	id: UUID
	product_id: UUID
	price: float
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
	price: float


class CreateOfferScheduleSchema(BaseModel):
	day: Day
	start_time: str = Field(min_length=6, max_length=8)
	end_time: str = Field(min_length=6, max_length=8)
	repeats: bool


class CreateOfferScheduleResponseSchema(BaseModel):
	id: UUID


class UpdateOfferScheduleSchema(BaseModel):
	day: Day
	start_time: str = Field(min_length=6, max_length=8)
	end_time: str = Field(min_length=6, max_length=8)
	repeats: bool
