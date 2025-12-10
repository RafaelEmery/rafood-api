from uuid import UUID

from src.users.exceptions import UserNotFoundError, UsersInternalError
from src.users.repository import UserRepository
from src.users.schemas import (
	CreateUserResponseSchema,
	CreateUserSchema,
	UpdateUserSchema,
	UserDetailsSchema,
	UserSchema,
)


class UserService:
	repository: UserRepository

	def __init__(self, repository: UserRepository):
		self.repository = repository

	async def list(self) -> list[UserSchema]:
		try:
			return await self.repository.list()
		except Exception as e:
			raise UsersInternalError(message=str(e)) from e

	# TODO: return restaurants on user details
	async def get(self, id: UUID) -> UserDetailsSchema:
		try:
			return await self.repository.get(id)
		except UserNotFoundError:
			raise
		except Exception as e:
			raise UsersInternalError(message=str(e)) from e

	async def create(self, user: CreateUserSchema) -> CreateUserResponseSchema:
		try:
			user_id = await self.repository.create(user)

			return CreateUserResponseSchema(id=user_id)
		except Exception as e:
			raise UsersInternalError(message=str(e)) from e

	async def update(self, id: UUID, user_update: UpdateUserSchema) -> UserSchema:
		try:
			user = await self.repository.get(id)

			user.first_name = user_update.first_name
			user.last_name = user_update.last_name

			await self.repository.update(user)

			return user
		except UserNotFoundError:
			raise
		except Exception as e:
			raise UsersInternalError(message=str(e)) from e

	async def delete(self, id: UUID) -> None:
		try:
			user = await self.repository.get(id)

			await self.repository.delete(user)
		except UserNotFoundError:
			raise
		except Exception as e:
			raise UsersInternalError(message=str(e)) from e
