from datetime import datetime
from uuid import UUID

from src.restaurants.repository import RestaurantRepository, RestaurantScheduleRepository
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


class RestaurantService:
	repository: RestaurantRepository

	def __init__(self, repository: RestaurantRepository):
		self.repository = repository

	async def list(
		self, name: str | None, owner_id: UUID | None
	) -> list[RestaurantWithSchedulesSchema]:
		return await self.repository.list(name, owner_id)

	async def get(self, id: UUID) -> RestaurantWithProductsSchema:
		return await self.repository.get(id)

	async def create(self, restaurant: CreateRestaurantSchema) -> CreateRestaurantResponseSchema:
		restaurant_id = await self.repository.create(restaurant)

		return CreateRestaurantResponseSchema(id=restaurant_id)

	async def update(self, id: UUID, restaurant_update: UpdateRestaurantSchema) -> RestaurantSchema:
		restaurant = await self.repository.get(id)

		restaurant.name = restaurant_update.name
		restaurant.image_url = restaurant_update.image_url
		restaurant.owner_id = restaurant_update.owner_id
		restaurant.street = restaurant_update.street
		restaurant.number = restaurant_update.number
		restaurant.neighborhood = restaurant_update.neighborhood
		restaurant.city = restaurant_update.city
		restaurant.state_abbr = restaurant_update.state_abbr

		await self.repository.update(restaurant)

		return restaurant

	async def delete(self, id: UUID) -> None:
		restaurant = await self.repository.get(id)

		await self.repository.delete(restaurant)


class RestaurantScheduleService:
	repository: RestaurantScheduleRepository
	restaurant_repository: RestaurantRepository

	def __init__(
		self, repository: RestaurantScheduleRepository, restaurant_repository: RestaurantRepository
	):
		self.repository = repository
		self.restaurant_repository = restaurant_repository

	# TODO: add validation to don't create schedule when there's three active schedules
	async def create(
		self, restaurant_id: UUID, schedule: CreateRestaurantScheduleSchema
	) -> CreateRestaurantScheduleResponseSchema:
		restaurant = await self.restaurant_repository.get(restaurant_id)
		schedule_id = await self.repository.create(schedule, restaurant.id)

		return CreateRestaurantScheduleResponseSchema(id=schedule_id)

	async def update(
		self,
		restaurant_id: UUID,
		schedule_id: UUID,
		schedule_update: UpdateRestaurantScheduleSchema,
	) -> RestaurantScheduleSchema:
		await self.restaurant_repository.get(restaurant_id)
		schedule = await self.repository.get(schedule_id)

		schedule.day_type = schedule_update.day_type.value
		schedule.start_day = schedule_update.start_day.value
		schedule.end_day = schedule_update.end_day.value
		schedule.start_time = datetime.strptime(schedule_update.start_time, '%H:%M:%S').time()
		schedule.end_time = datetime.strptime(schedule_update.end_time, '%H:%M:%S').time()

		await self.repository.update(schedule)

		return schedule

	async def delete(self, restaurant_id: UUID, schedule_id: UUID) -> None:
		await self.restaurant_repository.get(restaurant_id)
		schedule = await self.repository.get(schedule_id)

		await self.repository.delete(schedule)
