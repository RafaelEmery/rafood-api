from uuid import UUID

from src.products.repository import ProductRepository
from src.products.schemas import (
	CreateProductResponseSchema,
	CreateProductSchema,
	ProductSchema,
	ProductWithCategoriesSchema,
	UpdateProductSchema,
)


class ProductService:
	repository: ProductRepository

	def __init__(self, repository: ProductRepository):
		self.repository = repository

	async def list(
		self, name: str | None, category_id: UUID | None
	) -> list[ProductWithCategoriesSchema]:
		return await self.repository.list(name, category_id)

	# TODO: Validate if can return offers or some flag to offers
	async def get(self, id: UUID) -> ProductSchema:
		return await self.repository.get(id)

	async def create(self, product: CreateProductSchema) -> CreateProductResponseSchema:
		product_id = await self.repository.create(product)

		return CreateProductResponseSchema(id=product_id)

	async def update(self, id: UUID, product_update: UpdateProductSchema) -> ProductSchema:
		product = await self.repository.get(id)

		product.restaurant_id = product_update.restaurant_id
		product.name = product_update.name
		product.price = product_update.price
		product.category_id = product_update.category_id
		product.image_url = product_update.image_url

		await self.repository.update(product)

		return product

	async def delete(self, id: UUID) -> None:
		product = await self.repository.get(id)

		await self.repository.delete(product)
