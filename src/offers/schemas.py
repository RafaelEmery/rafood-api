from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field


class OfferSchema(BaseModel):
	id: UUID
	product_id: UUID
	price: float
	created_at: datetime
	updated_at: datetime

	# TODO: validate if orm_mode is really useful
	class Config:
		orm_mode = True


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
	start_time: str
	end_time: str
	repeats: bool
	created_at: datetime
	updated_at: datetime

	class Config:
		orm_mode = True


class CreateOfferScheduleSchema(BaseModel):
	offer_id: UUID
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