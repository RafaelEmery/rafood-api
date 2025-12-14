from uuid import UUID

from src.products.exceptions import ProductNotFoundError, ProductsInternalError
from src.products.repository import ProductRepository
from src.products.schemas import (
	CreateProductResponseSchema,
	CreateProductSchema,
	ProductSchema,
	ProductWithCategoriesSchema,
	ProductWithOffersSchema,
	UpdateProductSchema,
)


class ProductService:
	repository: ProductRepository

	def __init__(self, repository: ProductRepository):
		self.repository = repository

	async def list(
		self, name: str | None, category_id: UUID | None
	) -> list[ProductWithCategoriesSchema]:
		try:
			return await self.repository.list(name, category_id)
		except Exception as e:
			raise ProductsInternalError(message=str(e)) from e

	async def get(self, id: UUID) -> ProductWithOffersSchema:
		try:
			return await self.repository.get(id)
		except ProductNotFoundError:
			raise
		except Exception as e:
			raise ProductsInternalError(message=str(e)) from e

	async def create(self, product: CreateProductSchema) -> CreateProductResponseSchema:
		try:
			product_id = await self.repository.create(product)

			return CreateProductResponseSchema(id=product_id)
		except Exception as e:
			raise ProductsInternalError(message=str(e)) from e

	async def update(self, id: UUID, product_update: UpdateProductSchema) -> ProductSchema:
		try:
			product = await self.repository.get(id)

			product.restaurant_id = product_update.restaurant_id
			product.name = product_update.name
			product.price = product_update.price
			product.category_id = product_update.category_id
			product.image_url = product_update.image_url

			await self.repository.update(product)

			return product
		except ProductNotFoundError:
			raise
		except Exception as e:
			raise ProductsInternalError(message=str(e)) from e

	async def delete(self, id: UUID) -> None:
		try:
			product = await self.repository.get(id)

			await self.repository.delete(product)
		except ProductNotFoundError:
			raise
		except Exception as e:
			raise ProductsInternalError(message=str(e)) from e
