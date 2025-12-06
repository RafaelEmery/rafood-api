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
		result = await self.db.execute(select(Category))
		categories: list[Category] = result.scalars().unique().all()

		return categories

	async def get(self, id: UUID) -> Category:
		result = await self.db.execute(select(Category).where(Category.id == id))
		category: Category = result.scalars().unique().first()

		if not category:
			raise CategoryNotFoundError('Category not found')

		return category

	async def create(self, category: CreateCategorySchema) -> UUID:
		new_category = Category(**category.model_dump())

		self.db.add(new_category)
		await self.db.commit()

		return new_category.id

	async def delete(self, category: Category) -> None:
		await self.db.delete(category)
		await self.db.commit()
