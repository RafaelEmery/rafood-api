from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, HttpUrl, field_validator

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
	name: str = Field(min_length=1, max_length=256)
	price: float = Field(gt=0)
	category_id: UUID
	image_url: HttpUrl | None = None

	@field_validator('image_url')
	@classmethod
	def convert_url_to_string(cls, v):
		"""Convert HttpUrl to string for database storage"""
		if v is not None:
			return str(v)
		return v


class CreateProductResponseSchema(BaseModel):
	id: UUID


class UpdateProductSchema(CreateProductSchema):
	pass
