from uuid import UUID

from src.categories.exceptions import CategoriesInternalError, CategoryNotFoundError
from src.categories.repository import CategoryRepository
from src.categories.schemas import (
	CategorySchema,
	CreateCategoryResponseSchema,
	CreateCategorySchema,
)


class CategoryService:
	repository: CategoryRepository

	def __init__(self, repository: CategoryRepository):
		self.repository = repository

	async def list(self) -> list[CategorySchema]:
		try:
			return await self.repository.list()
		except Exception as e:
			raise CategoriesInternalError(message=str(e)) from e

	async def create(self, category: CreateCategorySchema) -> CreateCategoryResponseSchema:
		try:
			category_id = await self.repository.create(category)

			return CreateCategoryResponseSchema(id=category_id)
		except Exception as e:
			raise CategoriesInternalError(message=str(e)) from e

	async def delete(self, id: UUID) -> None:
		try:
			category = await self.repository.get(id)
			await self.repository.delete(category)
		except CategoryNotFoundError:
			raise
		except Exception as e:
			raise CategoriesInternalError(message=str(e)) from e
