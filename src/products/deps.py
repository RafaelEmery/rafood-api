from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.deps import get_session
from src.products.repository import ProductRepository
from src.products.service import ProductService


def get_product_repository(
	db: AsyncSession = Depends(get_session),
) -> ProductRepository:
	return ProductRepository(db)


def get_product_service(
	repository: ProductRepository = Depends(get_product_repository),
) -> ProductService:
	return ProductService(repository)


ProductServiceDeps = Annotated[ProductService, Depends(get_product_service)]
