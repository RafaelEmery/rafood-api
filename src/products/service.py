from uuid import UUID

from src.core.db.unit_of_work import UnitOfWork
from src.core.logging.logger import StructLogger
from src.core.outbox.service import OutboxService
from src.products.exceptions import ProductNotFoundError, ProductsInternalError
from src.products.outbox_events import ProductOutboxEvent, build_product_outbox_event
from src.products.repository import ProductRepository
from src.products.schemas import (
	CreateProductResponseSchema,
	CreateProductSchema,
	ProductSchema,
	ProductWithCategoriesSchema,
	ProductWithOffersSchema,
	UpdateProductSchema,
)

logger = StructLogger()


class ProductService:
	repository: ProductRepository
	outbox_service: OutboxService
	uow: UnitOfWork

	def __init__(
		self,
		repository: ProductRepository,
		outbox_service: OutboxService,
		uow: UnitOfWork,
	):
		self.repository = repository
		self.outbox_service = outbox_service
		self.uow = uow

	async def list(
		self, name: str | None, category_id: UUID | None
	) -> list[ProductWithCategoriesSchema]:
		try:
			products = await self.repository.list(name, category_id)
			logger.bind(listed_products_count=len(products))

			return [ProductWithCategoriesSchema.model_validate(product) for product in products]
		except Exception as e:
			raise ProductsInternalError(message=str(e)) from e

	async def get(self, id: UUID) -> ProductWithOffersSchema:
		try:
			product = await self.repository.get(id)
			logger.bind(retrieved_product_id=product.id)

			return ProductWithOffersSchema.model_validate(product)
		except ProductNotFoundError:
			raise
		except Exception as e:
			raise ProductsInternalError(message=str(e)) from e

	async def create(self, product: CreateProductSchema) -> CreateProductResponseSchema:
		try:
			created_product = await self.repository.create(product)
			self.outbox_service.create(
				build_product_outbox_event(created_product, ProductOutboxEvent.CREATED)
			)
			await self.uow.commit()
			logger.bind(created_product_id=str(created_product.id))

			return CreateProductResponseSchema(id=created_product.id)
		except Exception as e:
			await self.uow.rollback()
			raise ProductsInternalError(message=str(e)) from e

	async def update(self, id: UUID, product_update: UpdateProductSchema) -> ProductSchema:
		try:
			product = await self.repository.get(id)

			product.restaurant_id = product_update.restaurant_id
			product.name = product_update.name
			product.price = product_update.price
			product.category_id = product_update.category_id
			product.image_url = (
				str(product_update.image_url) if product_update.image_url is not None else None
			)

			await self.repository.update(product)
			self.outbox_service.create(
				build_product_outbox_event(product, ProductOutboxEvent.UPDATED)
			)
			await self.uow.commit()
			logger.bind(updated_product_id=product.id)

			return ProductSchema.model_validate(product)
		except ProductNotFoundError:
			raise
		except Exception as e:
			await self.uow.rollback()
			raise ProductsInternalError(message=str(e)) from e

	async def delete(self, id: UUID) -> None:
		try:
			product = await self.repository.get(id)
			self.outbox_service.create(
				build_product_outbox_event(product, ProductOutboxEvent.DELETED)
			)
			await self.repository.delete(product)
			await self.uow.commit()
			logger.bind(deleted_product_id=id)
		except ProductNotFoundError:
			raise
		except Exception as e:
			await self.uow.rollback()
			raise ProductsInternalError(message=str(e)) from e
