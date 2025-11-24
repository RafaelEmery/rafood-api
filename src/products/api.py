from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session
from products.models import Product
from products.schemas import (
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
	description='Get all products',
	response_model=list[ProductWithCategoriesSchema],
)
async def list_products(
	name: str | None = None,
	category_id: UUID | None = None,
	db: AsyncSession = Depends(get_session),
):
	async with db as session:
		try:
			query = select(Product)
			if name is not None:
				query = query.filter(Product.name.like(f'%{name}%'))
			if category_id is not None:
				query = query.filter(Product.category_id == category_id)

			result = await session.execute(query)
			products: list[ProductWithCategoriesSchema] = result.scalars().unique().all()

			return products
		except Exception as e:
			raise HTTPException(
				status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
			) from e


@router.get(
	'/{id}',
	name='Get product by ID',
	status_code=status.HTTP_200_OK,
	description='Get a product by ID',
	response_model=ProductSchema,
)
async def find_product(id: UUID, db: AsyncSession = Depends(get_session)):
	async with db as session:
		try:
			result = await session.execute(select(Product).where(Product.id == id))
			product: ProductSchema = result.scalars().first()

			# TODO: Validate if can return offers or some flag to offers

			if not product:
				raise HTTPException(
					status_code=status.HTTP_404_NOT_FOUND, detail='Product not found'
				)

			return product
		except Exception as e:
			raise HTTPException(
				status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
			) from e


@router.post(
	'',
	name='Create product',
	status_code=status.HTTP_201_CREATED,
	description='Create a new product',
	response_model=CreateProductResponseSchema,
)
async def create_product(product: CreateProductSchema, db: AsyncSession = Depends(get_session)):
	async with db as session:
		try:
			new_product = Product(**product.model_dump())

			session.add(new_product)
			await session.commit()

			return CreateProductResponseSchema(id=new_product.id)
		except Exception as e:
			raise HTTPException(
				status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
			) from e


@router.patch(
	'/{id}',
	name='Update product',
	status_code=status.HTTP_200_OK,
	description='Update a product by ID',
	response_model=ProductSchema,
)
async def update_product(
	id: UUID, body: UpdateProductSchema, db: AsyncSession = Depends(get_session)
):
	async with db as session:
		try:
			result = await session.execute(select(Product).where(Product.id == id))
			product: Product = result.scalars().first()

			if not product:
				raise HTTPException(
					status_code=status.HTTP_404_NOT_FOUND, detail='Product not found'
				)

			product.restaurant_id = body.restaurant_id
			product.name = body.name
			product.price = body.price
			product.category_id = body.category_id
			product.image_url = body.image_url
			await session.commit()

			return product
		except Exception as e:
			raise HTTPException(
				status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
			) from e


@router.delete(
	'/{id}',
	name='Delete product',
	status_code=status.HTTP_204_NO_CONTENT,
	description='Delete a product by ID',
)
async def delete_product(id: UUID, db: AsyncSession = Depends(get_session)):
	async with db as session:
		try:
			result = await session.execute(select(Product).where(Product.id == id))
			product: Product = result.scalars().first()

			if not product:
				raise HTTPException(
					status_code=status.HTTP_404_NOT_FOUND, detail='Product not found'
				)

			await session.delete(product)
			await session.commit()
		except Exception as e:
			raise HTTPException(
				status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
			) from e
