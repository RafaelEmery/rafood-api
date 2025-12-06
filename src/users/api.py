from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from src.exceptions import UserNotFoundError
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
async def list_users(service: UserServiceDeps):
	try:
		return await service.list()
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.get(
	'/{id}',
	name='Find user',
	status_code=status.HTTP_200_OK,
	description='Get a user by id with all its restaurants',
	response_model=UserDetailsSchema,
)
async def find_user(id: UUID, service: UserServiceDeps):
	try:
		return await service.get(id)
	except UserNotFoundError as e:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.post(
	'',
	name='Create user',
	status_code=status.HTTP_201_CREATED,
	description='Create a new user',
	response_model=CreateUserResponseSchema,
)
async def create_user(user: CreateUserSchema, service: UserServiceDeps):
	try:
		return await service.create(user)
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.put(
	'/{id}',
	name='Update user',
	status_code=status.HTTP_200_OK,
	description='Update a user by ID',
	response_model=UserSchema,
)
async def update_user(id: UUID, user_update: UpdateUserSchema, service: UserServiceDeps):
	try:
		return await service.update(id, user_update)
	except UserNotFoundError as e:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.delete(
	'/{id}',
	name='Delete user',
	status_code=status.HTTP_204_NO_CONTENT,
	description='Delete a user by ID',
)
async def delete_user(id: UUID, service: UserServiceDeps):
	try:
		await service.delete(id)
	except UserNotFoundError as e:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e
