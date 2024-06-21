from uuid import UUID
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, HttpUrl


# TODO: improve validation rules
# TODO: validate changing UUID from pydantic UUID4
class ProductSchema(BaseModel):
	id: UUID
	restaurant_id: UUID
	name: str
	price: float
	category_id: UUID
	image_url: Optional[HttpUrl] = None
	created_at: datetime
	updated_at: datetime

	# TODO: validate not using from_attributes
	class Config:
		from_attributes = True


class CreateProductSchema(BaseModel):
	restaurant_id: UUID
	name: str
	price: float
	category_id: UUID
	image_url: Optional[HttpUrl] = None


class CreateProductResponseSchema(BaseModel):
	id: UUID


class UpdateProductSchema(BaseModel):
	restaurant_id: UUID
	name: str
	price: float
	category_id: UUID
	image_url: Optional[HttpUrl] = None
