from uuid import UUID

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
		return await self.repository.list()

	async def create(self, category: CreateCategorySchema) -> CreateCategoryResponseSchema:
		category_id = await self.repository.create(category)

		return CreateCategoryResponseSchema(id=category_id)

	async def delete(self, id: UUID) -> None:
		category = await self.repository.get(id)
		await self.repository.delete(category)
