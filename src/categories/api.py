from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from src.categories.deps import CategoryServiceDeps
from src.categories.schemas import (
	CategorySchema,
	CreateCategoryResponseSchema,
	CreateCategorySchema,
)
from src.exceptions import CategoryNotFoundError

router = APIRouter()


@router.get(
	'',
	name='Get categories',
	status_code=status.HTTP_200_OK,
	description='Get all categories',
	response_model=list[CategorySchema],
)
async def list_category(service: CategoryServiceDeps):
	try:
		return await service.list()
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.post(
	'',
	name='Create category',
	status_code=status.HTTP_201_CREATED,
	description='Create a new category',
	response_model=CreateCategoryResponseSchema,
)
async def create_category(category: CreateCategorySchema, service: CategoryServiceDeps):
	try:
		return await service.create(category)
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.delete(
	'/{category_id}',
	name='Delete category',
	status_code=status.HTTP_204_NO_CONTENT,
	description='Delete a category by id',
)
async def delete_category(category_id: UUID, service: CategoryServiceDeps):
	try:
		await service.delete(category_id)
	except CategoryNotFoundError as e:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e
