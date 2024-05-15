from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .models import User
from .schemas import UserSchema, CreateUserSchema, CreateUserResponseSchema, UpdateUserSchema
from deps import get_session


router = APIRouter()


@router.get(
	'/',
	name='Get users',
	status_code=status.HTTP_200_OK,
	description='Get all users',
	response_model=List[UserSchema],
)
async def get_all_users(db: AsyncSession = Depends(get_session)):
	async with db as session:
		try:
			result = await session.execute(select(User))
			users: List[UserSchema] = result.scalars().all()

			return users
		except Exception as e:
			raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get(
	'/{user_id}',
	name='Get user by ID',
	status_code=status.HTTP_200_OK,
	description='Get a user by id with all its restaurants',
	response_model=UserSchema,
)
async def get_user(user_id: str, db: AsyncSession = Depends(get_session)):
	try:
		async with db as session:
			result = await session.execute(select(User).where(User.id == user_id))
			user: UserSchema = result.scalars().first()

			# TODO: load restaurants relationship

			if not user:
				raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

			return user
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post(
	'/',
	name='Create user',
	status_code=status.HTTP_201_CREATED,
	description='Create a new user',
	response_model=CreateUserResponseSchema,
)
async def create_user(user: CreateUserSchema, db: AsyncSession = Depends(get_session)):
	try:
		async with db as session:
			new_user = User(**user.model_dump())

			session.add(new_user)
			await session.commit()

			return CreateUserResponseSchema(id=new_user.id)
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put(
	'/{user_id}',
	name='Update user',
	status_code=status.HTTP_200_OK,
	description='Update a user by id',
	response_model=UserSchema,
)
async def update_user(
	user_id: str, body: UpdateUserSchema, db: AsyncSession = Depends(get_session)
):
	try:
		async with db as session:
			result = await session.execute(select(User).where(User.id == user_id))
			user: User = result.scalars().first()

			if not user:
				raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

			user.first_name = body.first_name
			user.last_name = body.last_name
			await session.commit()

			return user
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete(
	'/{user_id}',
	name='Delete user',
	status_code=status.HTTP_204_NO_CONTENT,
	description='Delete a user by id',
)
async def delete_user(user_id: str, db: AsyncSession = Depends(get_session)):
	async with db as session:
		try:
			result = await session.execute(select(User).where(User.id == user_id))
			user: User = result.scalars().first()

			if not user:
				raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

			session.delete(user)
			await session.commit()
		except Exception as e:
			raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
