from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl


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
