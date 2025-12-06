from uuid import UUID

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
		return await self.repository.list()

	# TODO: return restaurants on user details
	async def get(self, id: UUID) -> UserDetailsSchema:
		return await self.repository.get(id)

	async def create(self, user: CreateUserSchema) -> CreateUserResponseSchema:
		user_id = await self.repository.create(user)

		return CreateUserResponseSchema(id=user_id)

	async def update(self, id: UUID, user_update: UpdateUserSchema) -> UserSchema:
		user = await self.repository.get(id)

		user.first_name = user_update.first_name
		user.last_name = user_update.last_name

		await self.repository.update(user)

		return user

	async def delete(self, id: UUID) -> None:
		user = await self.repository.get(id)

		await self.repository.delete(user)
