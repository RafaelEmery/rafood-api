from uuid import UUID

from fastapi import APIRouter, status

from src.users.deps import UserServiceDeps
from src.users.schemas import (
	CreateUserResponseSchema,
	CreateUserSchema,
	UpdateUserSchema,
	UserDetailsSchema,
	UserSchema,
)

router = APIRouter()


@router.get(
	'',
	name='List users',
	status_code=status.HTTP_200_OK,
	description='Get all users',
	response_model=list[UserSchema],
)
async def list_users(service: UserServiceDeps) -> list[UserSchema]:
	return await service.list()


@router.get(
	'/{id}',
	name='Find user',
	status_code=status.HTTP_200_OK,
	description='Get a user by id with all its restaurants',
	response_model=UserDetailsSchema,
)
async def find_user(id: UUID, service: UserServiceDeps) -> UserDetailsSchema:
	return await service.get(id)


@router.post(
	'',
	name='Create user',
	status_code=status.HTTP_201_CREATED,
	description='Create a new user',
	response_model=CreateUserResponseSchema,
)
async def create_user(user: CreateUserSchema, service: UserServiceDeps) -> CreateUserResponseSchema:
	return await service.create(user)


@router.put(
	'/{id}',
	name='Update user',
	status_code=status.HTTP_200_OK,
	description='Update a user by ID',
	response_model=UserSchema,
)
async def update_user(
	id: UUID, user_update: UpdateUserSchema, service: UserServiceDeps
) -> UserSchema:
	return await service.update(id, user_update)


@router.delete(
	'/{id}',
	name='Delete user',
	status_code=status.HTTP_204_NO_CONTENT,
	description='Delete a user by ID',
)
async def delete_user(id: UUID, service: UserServiceDeps) -> None:
	await service.delete(id)
