from uuid import UUID

from fastapi import APIRouter, status

from src.categories.deps import CategoryServiceDeps
from src.categories.schemas import (
	CategorySchema,
	CreateCategoryResponseSchema,
	CreateCategorySchema,
)

router = APIRouter()


@router.get(
	'',
	name='Get categories',
	status_code=status.HTTP_200_OK,
	description='Get all categories',
	response_model=list[CategorySchema],
)
async def list_category(service: CategoryServiceDeps):
	return await service.list()


@router.post(
	'',
	name='Create category',
	status_code=status.HTTP_201_CREATED,
	description='Create a new category',
	response_model=CreateCategoryResponseSchema,
)
async def create_category(category: CreateCategorySchema, service: CategoryServiceDeps):
	return await service.create(category)


@router.delete(
	'/{category_id}',
	name='Delete category',
	status_code=status.HTTP_204_NO_CONTENT,
	description='Delete a category by id',
)
async def delete_category(category_id: UUID, service: CategoryServiceDeps):
	await service.delete(category_id)
