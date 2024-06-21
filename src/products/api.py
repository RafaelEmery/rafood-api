from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .models import Product
from .schemas import (
	ProductSchema,
	CreateProductSchema,
	CreateProductResponseSchema,
	UpdateProductSchema,
)
from core.deps import get_session


router = APIRouter()


@router.get(
	'/',
	name='Get products',
	status_code=status.HTTP_200_OK,
	description='Get all products',
	response_model=List[ProductSchema],
)
async def get_all_products(db: AsyncSession = Depends(get_session)):
	async with db as session:
		try:
			result = await session.execute(select(Product))
			products: List[ProductSchema] = result.scalars.all()

			return products
		except Exception as e:
			raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get(
	'/{product_id}',
	name='Get product by ID',
	status_code=status.HTTP_200_OK,
	description='Get a product by id',
	response_model=ProductSchema,
)
async def get_product(product_id: str, db: AsyncSession = Depends(get_session)):
	async with db as session:
		try:
			result = await session.execute(select(Product).where(Product.id == product_id))
			product: ProductSchema = result.scalars().first()

			# TODO: Validate if can return offers or some flag to offers

			if not product:
				raise HTTPException(
					status_code=status.HTTP_404_NOT_FOUND, detail='Product not found'
				)

			return product
		except Exception as e:
			raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post(
	'/',
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
			raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.patch(
	'/{product_id}',
	name='Update product',
	status_code=status.HTTP_200_OK,
	description='Update a product by id',
	response_model=ProductSchema,
)
async def update_product(
	product_id: str, body: UpdateProductSchema, db: AsyncSession = Depends(get_session)
):
	async with db as session:
		try:
			result = await session.execute(select(Product).where(Product.id == product_id))
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
			raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete(
	'/{product_id}',
	name='Delete product',
	status_code=status.HTTP_204_NO_CONTENT,
	description='Delete a product by id',
)
async def delete_product(product_id: str, db: AsyncSession = Depends(get_session)):
	async with db as session:
		try:
			result = await session.execute(select(Product).where(Product.id == product_id))
			product: Product = result.scalars().first()

			if not product:
				raise HTTPException(
					status_code=status.HTTP_404_NOT_FOUND, detail='Product not found'
				)

			await session.delete(product)
			await session.commit()
		except Exception as e:
			raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
