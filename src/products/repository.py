from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.exceptions import ProductNotFoundError
from src.products.models import Product
from src.products.schemas import CreateProductSchema


class ProductRepository:
	db: AsyncSession

	def __init__(self, db: AsyncSession):
		self.db = db

	async def list(self, name: str | None, category_id: UUID | None) -> list[Product]:
		query = select(Product)

		if name is not None:
			query = query.filter(Product.name.contains(name))
		if category_id is not None:
			query = query.filter(Product.category_id == category_id)

		result = await self.db.execute(query)

		return result.scalars().unique().all()

	async def get(self, id: UUID) -> Product:
		result = await self.db.execute(select(Product).where(Product.id == id))
		product = result.scalars().unique().first()

		if not product:
			raise ProductNotFoundError('Product not found')

		return product

	async def create(self, product: CreateProductSchema) -> UUID:
		new_product = Product(**product.model_dump())

		self.db.add(new_product)
		await self.db.commit()

		return new_product.id

	async def update(self, product: Product) -> None:
		self.db.add(product)

		await self.db.commit()
		await self.db.refresh(product)

	async def delete(self, product: Product) -> None:
		await self.db.delete(product)
		await self.db.commit()
