from uuid import UUID
from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, EmailStr

from restaurants.schemas import RestaurantSchema


class UserSchema(BaseModel):
	id: UUID
	first_name: str
	last_name: str
	email: EmailStr
	created_at: datetime
	updated_at: datetime

	class Config:
		from_attributes = True


class UserDetailsSchema(UserSchema):
	restaurants: List[RestaurantSchema] = []


class CreateUserSchema(BaseModel):
	first_name: str = Field(max_length=256)
	last_name: str = Field(max_length=256)
	email: EmailStr
	password: str = Field(max_length=256)


class CreateUserResponseSchema(BaseModel):
	id: UUID


class UpdateUserSchema(BaseModel):
	first_name: str = Field(max_length=256)
	last_name: str = Field(max_length=256)
