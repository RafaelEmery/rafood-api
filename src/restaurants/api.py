from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .models import Restaurant, RestaurantSchedule
from .schemas import (
	RestaurantSchema,
	RestaurantScheduleSchema,
	CreateRestaurantSchema,
	CreateRestaurantResponseSchema,
	CreateRestaurantScheduleSchema,
	UpdateRestaurantScheduleSchema,
	CreateRestaurantScheduleResponseSchema,
	UpdateRestaurantSchema,
)
from core.deps import get_session


router = APIRouter()


@router.get(
	'/',
	status_code=status.HTTP_200_OK,
	description='Get all restaurants',
	response_model=List[RestaurantSchema],
)
async def get_all_restaurants(db: AsyncSession = Depends(get_session)):
	async with db as session:
		try:
			result = await session.execute(select(Restaurant))
			restaurants: List[RestaurantSchema] = result.scalars().all()

			return restaurants
		except Exception as e:
			raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get(
	'/{restaurant_id}',
	status_code=status.HTTP_200_OK,
	description='Get a restaurant by id with owner and schedules',
	response_model=RestaurantSchema,
)
async def get_restaurant(restaurant_id: str, db: AsyncSession = Depends(get_session)):
	async with db as session:
		try:
			result = await session.execute(select(Restaurant).where(Restaurant.id == restaurant_id))
			restaurant: RestaurantSchema = result.scalars().first()

			# TODO: load schedule and owner relationships

			if not restaurant:
				raise HTTPException(
					status_code=status.HTTP_404_NOT_FOUND, detail='Restaurant not found'
				)

			return restaurant
		except Exception as e:
			raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# TODO: get only products relationship
@router.get(
	'/{restaurant_id}/products',
	status_code=status.HTTP_200_OK,
	description='Get all products from a restaurant',
)
async def get_restaurant_products(restaurant_id: str):
	return {'message': f'Get products from restaurant {restaurant_id}'}


# TODO: add owner_id validation
@router.post(
	'/',
	name='Create a restaurant',
	status_code=status.HTTP_201_CREATED,
	response_model=CreateRestaurantResponseSchema,
	description='Create a new restaurant',
)
async def create_restaurant(
	restaurant: CreateRestaurantSchema, db: AsyncSession = Depends(get_session)
):
	async with db as session:
		try:
			new_restaurant: Restaurant = Restaurant(**restaurant.model_dump())

			session.add(new_restaurant)
			await session.commit()

			return CreateRestaurantResponseSchema(id=new_restaurant.id)
		except Exception as e:
			raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.patch(
	'/{restaurant_id}',
	name='Update restaurant',
	status_code=status.HTTP_200_OK,
	description='Update a restaurant',
	response_model=RestaurantSchema,
)
async def update_restaurant(
	restaurant_id: str, body: UpdateRestaurantSchema, db: AsyncSession = Depends(get_session)
):
	async with db as session:
		try:
			result = await session.execute(select(Restaurant).where(Restaurant.id == restaurant_id))
			restaurant: Restaurant = result.scalars().first()

			if not restaurant:
				return HTTPException(
					status_code=status.HTTP_404_NOT_FOUND, detail='Restaurant not found'
				)

			# TODO: implement update methods using some more like a mass assignment
			restaurant.name = body.name
			restaurant.image_url = body.image_url
			restaurant.owner_id = body.owner_id
			restaurant.street = body.street
			restaurant.number = body.number
			restaurant.neighborhood = body.neighborhood
			restaurant.city = body.city
			restaurant.state_abbr = body.state_abbr

			await session.commit()

			return restaurant
		except Exception as e:
			raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete(
	'/{restaurant_id}',
	name='Delete restaurant',
	status_code=status.HTTP_204_NO_CONTENT,
	description='Delete a restaurant by id',
)
async def delete_restaurant(restaurant_id: str, db: AsyncSession = Depends(get_session)):
	async with db as session:
		try:
			result = await session.execute(select(Restaurant).where(Restaurant.id == restaurant_id))
			restaurant: Restaurant = result.scalars().first()

			if not restaurant:
				raise HTTPException(
					status_code=status.HTTP_404_NOT_FOUND, detail='Restaurant not found'
				)

			await session.delete(restaurant)
			await session.commit()
		except Exception as e:
			raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post(
	'/{restaurant_id}/schedules',
	name='Create a restaurant schedule',
	status_code=status.HTTP_201_CREATED,
	response_model=CreateRestaurantScheduleResponseSchema,
	description='Create a new restaurant',
)
async def create_restaurant_schedule(
	restaurant_id: str,
	schedule: CreateRestaurantScheduleSchema,
	db: AsyncSession = Depends(get_session),
):
	async with db as session:
		try:
			new_schedule: RestaurantSchedule = RestaurantSchedule(**schedule.model_dump())
			new_schedule.restaurant_id = restaurant_id
			new_schedule.start_time = datetime.strptime(schedule.start_time, '%H:%M:%S').time()
			new_schedule.end_time = datetime.strptime(schedule.end_time, '%H:%M:%S').time()

			# TODO: add validation to don't create schedule when there's three active schedules

			session.add(new_schedule)
			await session.commit()

			return CreateRestaurantScheduleResponseSchema(id=new_schedule.id)
		except Exception as e:
			raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.patch(
	'/{restaurant_id}/schedules/{schedule_id}',
	name='Update a restaurant schedule',
	status_code=status.HTTP_200_OK,
	response_model=RestaurantScheduleSchema,
	description='Update a restaurant schedule',
)
async def update_restaurant_schedule(
	restaurant_id: str,
	schedule_id: str,
	body: UpdateRestaurantScheduleSchema,
	db: AsyncSession = Depends(get_session),
):
	async with db as session:
		try:
			result = await session.execute(select(Restaurant).where(Restaurant.id == restaurant_id))
			restaurant: Restaurant = result.scalars().first()

			if not restaurant:
				return HTTPException(
					status_code=status.HTTP_404_NOT_FOUND, detail='Restaurant not found'
				)

			result = await session.execute(
				select(RestaurantSchedule).where(RestaurantSchedule.id == schedule_id)
			)
			schedule: RestaurantSchedule = result.scalars().first()

			if not schedule:
				return HTTPException(
					status_code=status.HTTP_404_NOT_FOUND, detail='Schedule not found'
				)

			# TODO: implement update methods using some more like a mass assignment
			schedule.day_type = body.day_type
			schedule.start_day = body.start_day
			schedule.end_day = body.end_day
			schedule.start_time = datetime.strptime(body.start_time, '%H:%M:%S').time()
			schedule.end_time = datetime.strptime(body.end_time, '%H:%M:%S').time()

			await session.commit()

			return schedule
		except Exception as e:
			raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete(
	'/{restaurant_id}/schedules/{schedule_id}',
	name='Delete a restaurant schedule',
	status_code=status.HTTP_204_NO_CONTENT,
	description='Delete a restaurant schedule',
)
async def delete_restaurant_schedule(
	restaurant_id: str, schedule_id: str, db: AsyncSession = Depends(get_session)
):
	async with db as session:
		try:
			result = await session.execute(select(Restaurant).where(Restaurant.id == restaurant_id))
			restaurant: Restaurant = result.scalars().first()

			if not restaurant:
				return HTTPException(
					status_code=status.HTTP_404_NOT_FOUND, detail='Restaurant not found'
				)

			result = await session.execute(
				select(RestaurantSchedule).where(RestaurantSchedule.id == schedule_id)
			)
			schedule: RestaurantSchedule = result.scalars().first()

			if not schedule:
				return HTTPException(
					status_code=status.HTTP_404_NOT_FOUND, detail='Schedule not found'
				)

			await session.delete(schedule)
			await session.commit()
		except Exception as e:
			raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
