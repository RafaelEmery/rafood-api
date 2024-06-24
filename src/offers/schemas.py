from uuid import UUID
from datetime import datetime, time

from pydantic import BaseModel, Field


class OfferSchema(BaseModel):
	id: UUID
	product_id: UUID
	price: float
	created_at: datetime
	updated_at: datetime

	class Config:
		from_attributes = True


class CreateOfferSchema(BaseModel):
	product_id: UUID
	price: float


class CreateOfferResponseSchema(BaseModel):
	id: UUID


# TODO: validate if user send null when is Optional[float] = None
class UpdateOfferSchema(BaseModel):
	price: float


class OfferScheduleSchema(BaseModel):
	id: UUID
	offer_id: UUID
	day: str
	start_time: time
	end_time: time
	repeats: bool
	created_at: datetime
	updated_at: datetime

	class Config:
		from_attributes = True
		json_encoders = {time: lambda v: v.strftime('%H:%M:%S')}


class CreateOfferScheduleSchema(BaseModel):
	day: str
	start_time: str = Field(min_length=6, max_length=8)
	end_time: str = Field(min_length=6, max_length=8)
	repeats: bool


class CreateOfferScheduleResponseSchema(BaseModel):
	id: UUID


class UpdateOfferScheduleSchema(BaseModel):
	day: str
	start_time: str = Field(min_length=6, max_length=8)
	end_time: str = Field(min_length=6, max_length=8)
	repeats: bool
