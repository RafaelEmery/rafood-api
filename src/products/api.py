from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from src.exceptions import ProductNotFoundError
from src.products.deps import ProductServiceDeps
from src.products.schemas import (
	CreateProductResponseSchema,
	CreateProductSchema,
	ProductSchema,
	ProductWithCategoriesSchema,
	UpdateProductSchema,
)

router = APIRouter()


@router.get(
	'',
	name='List products',
	status_code=status.HTTP_200_OK,
	response_model=list[ProductWithCategoriesSchema],
)
async def list_products(
	service: ProductServiceDeps, name: str | None = None, category_id: UUID | None = None
):
	try:
		return await service.list(name, category_id)
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.get(
	'/{id}',
	name='Find product',
	status_code=status.HTTP_200_OK,
	response_model=ProductSchema,
)
async def find_product(id: UUID, service: ProductServiceDeps):
	try:
		return await service.get(id)
	except ProductNotFoundError as e:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.post(
	'',
	name='Create product',
	status_code=status.HTTP_201_CREATED,
	response_model=CreateProductResponseSchema,
)
async def create_product(body: CreateProductSchema, service: ProductServiceDeps):
	try:
		return await service.create(body)
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.patch(
	'/{id}',
	name='Update product',
	status_code=status.HTTP_200_OK,
	response_model=ProductSchema,
)
async def update_product(
	id: UUID, product_update: UpdateProductSchema, service: ProductServiceDeps
):
	try:
		return await service.update(id, product_update)
	except ProductNotFoundError as e:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.delete(
	'/{id}',
	name='Delete product',
	status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_product(id: UUID, service: ProductServiceDeps):
	try:
		await service.delete(id)
	except ProductNotFoundError as e:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e
