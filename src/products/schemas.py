from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, HttpUrl
from categories.schemas import CategorySchema


# TODO: validate changing UUID from pydantic UUID4
class ProductSchema(BaseModel):
	id: UUID
	restaurant_id: UUID
	name: str
	price: float
	category_id: UUID
	image_url: str
	created_at: datetime
	updated_at: datetime

	class Config:
		from_attributes = True


class ProductWithCategories(ProductSchema):
	category: CategorySchema


# TODO: improve validation rules
class CreateProductSchema(BaseModel):
	restaurant_id: UUID
	name: str
	price: float
	category_id: UUID
	image_url: str = HttpUrl | None


class CreateProductResponseSchema(BaseModel):
	id: UUID


class UpdateProductSchema(BaseModel):
	restaurant_id: UUID
	name: str
	price: float
	category_id: UUID
	image_url: str = HttpUrl
