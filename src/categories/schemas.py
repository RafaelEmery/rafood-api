from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class CategorySchema(BaseModel):
	id: UUID
	name: str
	created_at: datetime
	updated_at: datetime

	class Config:
		from_attributes = True


class CreateCategorySchema(BaseModel):
	name: str = Field(min_length=1, max_length=256)


class CreateCategoryResponseSchema(BaseModel):
	id: UUID
