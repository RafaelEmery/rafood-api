from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .schemas import CategorySchema, CreateCategorySchema, CreateCategoryResponseSchema
from .models import Category
from core.deps import get_session


router = APIRouter()


@router.get(
	'/',
	name='Get categories',
	status_code=status.HTTP_200_OK,
	description='Get all categories',
	response_model=List[CategorySchema],
)
async def get_all_categories(db: AsyncSession = Depends(get_session)):
	try:
		async with db as session:
			result = await session.execute(select(Category))
			categories: List[CategorySchema] = result.scalars().all()

			return categories
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post(
	'/',
	name='Create category',
	status_code=status.HTTP_201_CREATED,
	description='Create a new category',
)
async def create_category(category: CreateCategorySchema, db: AsyncSession = Depends(get_session)):
	try:
		async with db as session:
			new_category = Category(**category.model_dump())

			session.add(new_category)
			await session.commit()

			return CreateCategoryResponseSchema(id=new_category.id)
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete(
	'/{category_id}',
	name='Delete category',
	status_code=status.HTTP_204_NO_CONTENT,
	description='Delete a category by id',
)
async def delete_category(category_id: str, db: AsyncSession = Depends(get_session)):
	try:
		async with db as session:
			result = await session.execute(select(Category).where(Category.id == category_id))
			category: Category = result.scalars().first()

			if not category:
				raise HTTPException(
					status_code=status.HTTP_404_NOT_FOUND, detail='Category not found'
				)

			await session.delete(category)
			await session.commit()
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
