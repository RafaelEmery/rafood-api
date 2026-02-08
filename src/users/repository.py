from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from src.users.exceptions import UserNotFoundError
from src.users.models import User
from src.users.schemas import CreateUserSchema


class UserRepository:
	db: AsyncSession

	def __init__(self, db: AsyncSession):
		self.db = db

	async def list(self) -> list[User]:
		result = await self.db.execute(select(User))
		users: list[User] = result.scalars().unique().all()  # type: ignore[assignment]

		return users

	async def get(self, id: UUID) -> User:
		query = select(User).options(selectinload(User.restaurants)).where(User.id == id)  # type: ignore[arg-type]
		result = await self.db.execute(query)
		user: User | None = result.scalars().unique().first()

		if not user:
			raise UserNotFoundError(user_id=str(id))

		return user

	async def create(self, user: CreateUserSchema) -> UUID:
		new_user = User(**user.model_dump())

		self.db.add(new_user)
		await self.db.commit()

		return new_user.id

	async def update(self, user: User) -> None:
		self.db.add(user)

		await self.db.commit()
		await self.db.refresh(user)

	async def delete(self, user: User) -> None:
		await self.db.delete(user)
		await self.db.commit()
