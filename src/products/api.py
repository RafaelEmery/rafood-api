from uuid import UUID

from fastapi import APIRouter, status

from src.products.deps import ProductServiceDeps
from src.products.schemas import (
	CreateProductResponseSchema,
	CreateProductSchema,
	ProductSchema,
	ProductWithCategoriesSchema,
	ProductWithOffersSchema,
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
) -> list[ProductWithCategoriesSchema]:
	return await service.list(name, category_id)


@router.get(
	'/{id}',
	name='Find product',
	status_code=status.HTTP_200_OK,
	response_model=ProductWithOffersSchema,
)
async def find_product(id: UUID, service: ProductServiceDeps) -> ProductWithOffersSchema:
	return await service.get(id)


@router.post(
	'',
	name='Create product',
	status_code=status.HTTP_201_CREATED,
	response_model=CreateProductResponseSchema,
)
async def create_product(
	body: CreateProductSchema, service: ProductServiceDeps
) -> CreateProductResponseSchema:
	return await service.create(body)


@router.patch(
	'/{id}',
	name='Update product',
	status_code=status.HTTP_200_OK,
	response_model=ProductSchema,
)
async def update_product(
	id: UUID, product_update: UpdateProductSchema, service: ProductServiceDeps
) -> ProductSchema:
	return await service.update(id, product_update)


@router.delete(
	'/{id}',
	name='Delete product',
	status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_product(id: UUID, service: ProductServiceDeps) -> None:
	await service.delete(id)
