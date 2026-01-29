from uuid import UUID

from src.core.logging.logger import StructLogger
from src.users.exceptions import UserNotFoundError, UsersInternalError
from src.users.repository import UserRepository
from src.users.schemas import (
	CreateUserResponseSchema,
	CreateUserSchema,
	UpdateUserSchema,
	UserDetailsSchema,
	UserSchema,
)

logger = StructLogger()


class UserService:
	repository: UserRepository

	def __init__(self, repository: UserRepository):
		self.repository = repository

	async def list(self) -> list[UserSchema]:
		try:
			users = await self.repository.list()
			logger.bind(listed_users_count=len(users))

			return users
		except Exception as e:
			raise UsersInternalError(message=str(e)) from e

	async def get(self, id: UUID) -> UserDetailsSchema:
		try:
			user = await self.repository.get(id)
			logger.bind(retrieved_user_id=user.id)

			return user
		except UserNotFoundError:
			raise
		except Exception as e:
			raise UsersInternalError(message=str(e)) from e

	async def create(self, user: CreateUserSchema) -> CreateUserResponseSchema:
		try:
			user_id = await self.repository.create(user)
			logger.bind(created_user_id=str(user_id))

			return CreateUserResponseSchema(id=user_id)
		except Exception as e:
			raise UsersInternalError(message=str(e)) from e

	async def update(self, id: UUID, user_update: UpdateUserSchema) -> UserSchema:
		try:
			user = await self.repository.get(id)

			user.first_name = user_update.first_name
			user.last_name = user_update.last_name

			await self.repository.update(user)
			logger.bind(updated_user_id=user.id)

			return user
		except UserNotFoundError:
			raise
		except Exception as e:
			raise UsersInternalError(message=str(e)) from e

	async def delete(self, id: UUID) -> None:
		try:
			user = await self.repository.get(id)

			await self.repository.delete(user)
			logger.bind(deleted_user_id=id)
		except UserNotFoundError:
			raise
		except Exception as e:
			raise UsersInternalError(message=str(e)) from e
