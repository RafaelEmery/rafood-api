from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

import src.core.outbox.models as _outbox_models  # noqa: F401
from src.core.db.unit_of_work import UnitOfWork
from src.core.deps import get_session, get_unit_of_work
from src.core.outbox.deps import get_outbox_repository
from src.core.outbox.repository import OutboxRepository
from src.products.repository import ProductRepository
from src.products.service import ProductService


def get_product_repository(
	db: AsyncSession = Depends(get_session),
) -> ProductRepository:
	return ProductRepository(db)


def get_product_service(
	repository: ProductRepository = Depends(get_product_repository),
	outbox_repository: OutboxRepository = Depends(get_outbox_repository),
	uow: UnitOfWork = Depends(get_unit_of_work),
) -> ProductService:
	return ProductService(repository, outbox_repository, uow)


ProductServiceDeps = Annotated[ProductService, Depends(get_product_service)]
