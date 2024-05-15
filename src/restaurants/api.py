from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from .models import Restaurant
from .schemas import CreateRestaurantSchema, CreateRestaurantResponseSchema
from deps import get_session


router = APIRouter()


@router.get('/', status_code=status.HTTP_200_OK, description='Get all restaurants')
async def get_all_restaurants():
	return {'message': 'Get all restaurants'}


# TODO: get schedule and owner relationships
@router.get(
	'/{restaurant_id}',
	status_code=status.HTTP_200_OK,
	description='Get a restaurant by id with owner and schedules',
)
async def get_restaurant(restaurant_id: str):
	return {'message': f'Get restaurant {restaurant_id}'}


# TODO: get only products relationship
@router.get(
	'/{restaurant_id}/products',
	status_code=status.HTTP_200_OK,
	description='Get all products from a restaurant',
)
async def get_restaurant_products(restaurant_id: str):
	return {'message': f'Get products from restaurant {restaurant_id}'}


@router.post(
	'/',
	status_code=status.HTTP_201_CREATED,
	response_model=CreateRestaurantResponseSchema,
	description='Create a new restaurant',
)
async def create_restaurant(
	restaurant: CreateRestaurantSchema, db: AsyncSession = Depends(get_session)
):
	# TODO: add owner_id validation
	# TODO: intercept pydantic validation exception and return custom payload
	# TODO: handle bad request and server error exceptions
	# TODO: abstract base exception payload for all endpoints
	try:
		async with db as session:
			new_restaurant = Restaurant(**restaurant.model_dump())

			session.add(new_restaurant)
			await session.commit()

			return CreateRestaurantResponseSchema(id=new_restaurant.id)
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put('/{restaurant_id}')
async def update_restaurant(restaurant_id: str):
	return {'message': f'Update restaurant {restaurant_id}'}


@router.delete('/{restaurant_id}')
async def delete_restaurant(restaurant_id: str):
	return {'message': f'Delete restaurant {restaurant_id}'}
