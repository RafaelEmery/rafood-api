from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, HttpUrl

from src.categories.schemas import CategorySchema


class ProductSchema(BaseModel):
	id: UUID
	restaurant_id: UUID
	name: str
	price: float
	category_id: UUID
	image_url: HttpUrl | None
	created_at: datetime
	updated_at: datetime

	class Config:
		from_attributes = True


class ProductWithCategoriesSchema(ProductSchema):
	category: CategorySchema


class CreateProductSchema(BaseModel):
	restaurant_id: UUID
	name: str
	price: float = Field(gt=0)
	category_id: UUID
	image_url: HttpUrl | None


class CreateProductResponseSchema(BaseModel):
	id: UUID


class UpdateProductSchema(BaseModel):
	restaurant_id: UUID
	name: str
	price: float = Field(gt=0)
	category_id: UUID
	image_url: HttpUrl | None
