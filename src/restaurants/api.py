from uuid import UUID

from fastapi import APIRouter, status

from src.restaurants.deps import (
	RestaurantScheduleServiceDeps,
	RestaurantServiceDeps,
)
from src.restaurants.schemas import (
	CreateRestaurantResponseSchema,
	CreateRestaurantScheduleResponseSchema,
	CreateRestaurantScheduleSchema,
	CreateRestaurantSchema,
	RestaurantScheduleSchema,
	RestaurantSchema,
	RestaurantWithProductsSchema,
	RestaurantWithSchedulesSchema,
	UpdateRestaurantScheduleSchema,
	UpdateRestaurantSchema,
)

router = APIRouter()


@router.get(
	'',
	name='List restaurants',
	status_code=status.HTTP_200_OK,
	response_model=list[RestaurantWithSchedulesSchema],
)
async def list_restaurants(
	service: RestaurantServiceDeps,
	name: str | None = None,
	owner_id: UUID | None = None,
):
	return await service.list(name=name, owner_id=owner_id)


@router.get(
	'/{id}',
	name='Find restaurant',
	status_code=status.HTTP_200_OK,
	response_model=RestaurantWithProductsSchema,
)
async def find_restaurant(id: UUID, service: RestaurantServiceDeps):
	return await service.get(id)


@router.post(
	'',
	name='Create a restaurant',
	status_code=status.HTTP_201_CREATED,
	response_model=CreateRestaurantResponseSchema,
)
async def create_restaurant(
	body: CreateRestaurantSchema,
	service: RestaurantServiceDeps,
):
	return await service.create(body)


@router.patch(
	'/{id}',
	name='Update restaurant',
	status_code=status.HTTP_200_OK,
	response_model=RestaurantSchema,
)
async def update_restaurant(
	id: UUID,
	body: UpdateRestaurantSchema,
	service: RestaurantServiceDeps,
):
	return await service.update(id, body)


@router.delete(
	'/{id}',
	name='Delete restaurant',
	status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_restaurant(id: UUID, service: RestaurantServiceDeps):
	await service.delete(id)


@router.post(
	'/{id}/schedules',
	name='Create restaurant schedule',
	status_code=status.HTTP_201_CREATED,
	response_model=CreateRestaurantScheduleResponseSchema,
)
async def create_restaurant_schedule(
	id: UUID,
	schedule: CreateRestaurantScheduleSchema,
	service: RestaurantScheduleServiceDeps,
):
	return await service.create(id, schedule)


@router.patch(
	'/{id}/schedules/{schedule_id}',
	name='Update restaurant schedule',
	status_code=status.HTTP_200_OK,
	response_model=RestaurantScheduleSchema,
)
async def update_restaurant_schedule(
	id: UUID,
	schedule_id: UUID,
	body: UpdateRestaurantScheduleSchema,
	service: RestaurantScheduleServiceDeps,
):
	return await service.update(id, schedule_id, body)


@router.delete(
	'/{id}/schedules/{schedule_id}',
	name='Delete restaurant schedule',
	status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_restaurant_schedule(
	id: UUID,
	schedule_id: UUID,
	service: RestaurantScheduleServiceDeps,
):
	await service.delete(id, schedule_id)
