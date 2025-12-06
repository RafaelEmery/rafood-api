from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.categories.repository import CategoryRepository
from src.categories.service import CategoryService
from src.core.deps import get_session


def get_category_repository(
	db: AsyncSession = Depends(get_session),
) -> CategoryRepository:
	return CategoryRepository(db)


def get_category_service(
	repository: CategoryRepository = Depends(get_category_repository),
) -> CategoryService:
	return CategoryService(repository)


CategoryServiceDeps = Annotated[CategoryService, Depends(get_category_service)]
