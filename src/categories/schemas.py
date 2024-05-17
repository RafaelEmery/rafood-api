from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class CategorySchema(BaseModel):
	id: UUID
	name: str
	created_at: datetime
	updated_at: datetime

	class Config:
		from_attributes = True


class CreateCategorySchema(BaseModel):
	name: str


class CreateCategoryResponseSchema(BaseModel):
	id: UUID
