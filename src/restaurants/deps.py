from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.deps import get_session
from src.restaurants.repository import (
	RestaurantRepository,
	RestaurantScheduleRepository,
)
from src.restaurants.service import (
	RestaurantScheduleService,
	RestaurantService,
)


def get_restaurant_repository(
	db: AsyncSession = Depends(get_session),
) -> RestaurantRepository:
	return RestaurantRepository(db)


def get_restaurant_service(
	repository: RestaurantRepository = Depends(get_restaurant_repository),
) -> RestaurantService:
	return RestaurantService(repository)


RestaurantServiceDeps = Annotated[RestaurantService, Depends(get_restaurant_service)]


def get_restaurant_schedule_repository(
	db: AsyncSession = Depends(get_session),
) -> RestaurantScheduleRepository:
	return RestaurantScheduleRepository(db)


def get_restaurant_schedule_service(
	repository: RestaurantScheduleRepository = Depends(get_restaurant_schedule_repository),
	restaurant_repository: RestaurantRepository = Depends(get_restaurant_repository),
) -> RestaurantScheduleService:
	return RestaurantScheduleService(repository, restaurant_repository)


RestaurantScheduleServiceDeps = Annotated[
	RestaurantScheduleService,
	Depends(get_restaurant_schedule_service),
]
