from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.categories.models import Category
from src.categories.schemas import CreateCategorySchema
from src.exceptions import CategoryNotFoundError


class CategoryRepository:
	db: AsyncSession

	def __init__(self, db: AsyncSession):
		self.db = db

	async def list(self) -> list[Category]:
		async with self.db as session:
			result = await session.execute(select(Category))
			categories: list[Category] = result.scalars().all()

			return categories

	async def get(self, id: UUID) -> Category:
		async with self.db as session:
			result = await session.execute(select(Category).where(Category.id == id))
			category: Category = result.scalars().first()

			if not category:
				raise CategoryNotFoundError('Category not found')

			return category

	async def create(self, category: CreateCategorySchema) -> UUID:
		async with self.db as session:
			new_category = Category(**category.model_dump())

			session.add(new_category)
			await session.commit()

			return new_category.id

	async def delete(self, category: Category) -> None:
		async with self.db as session:
			await session.delete(category)
			await session.commit()
