from datetime import datetime
from uuid import UUID

from src.core.logging.logger import StructLogger
from src.restaurants.exceptions import (
	RestaurantNotFoundError,
	RestaurantScheduleNotFoundError,
	RestaurantSchedulesInternalError,
	RestaurantsInternalError,
)
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

logger = StructLogger()


class RestaurantService:
	repository: RestaurantRepository

	def __init__(self, repository: RestaurantRepository):
		self.repository = repository

	async def list(
		self, name: str | None, owner_id: UUID | None
	) -> list[RestaurantWithSchedulesSchema]:
		try:
			restaurants = await self.repository.list(name, owner_id)
			logger.bind(listed_restaurants_count=len(restaurants))

			return restaurants
		except Exception as e:
			raise RestaurantsInternalError(message=str(e)) from e

	async def get(self, id: UUID) -> RestaurantWithProductsSchema:
		try:
			restaurant = await self.repository.get(id)
			logger.bind(retrieved_restaurant_id=restaurant.id)

			return restaurant
		except RestaurantNotFoundError:
			raise
		except Exception as e:
			raise RestaurantsInternalError(message=str(e)) from e

	async def create(self, restaurant: CreateRestaurantSchema) -> CreateRestaurantResponseSchema:
		try:
			restaurant_id = await self.repository.create(restaurant)
			logger.bind(created_restaurant_id=str(restaurant_id))

			return CreateRestaurantResponseSchema(id=restaurant_id)
		except Exception as e:
			raise RestaurantsInternalError(message=str(e)) from e

	async def update(self, id: UUID, restaurant_update: UpdateRestaurantSchema) -> RestaurantSchema:
		try:
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
			logger.bind(updated_restaurant_id=restaurant.id)

			return restaurant
		except RestaurantNotFoundError:
			raise
		except Exception as e:
			raise RestaurantsInternalError(message=str(e)) from e

	async def delete(self, id: UUID) -> None:
		try:
			restaurant = await self.repository.get(id)

			await self.repository.delete(restaurant)
			logger.bind(deleted_restaurant_id=id)
		except RestaurantNotFoundError:
			raise
		except Exception as e:
			raise RestaurantsInternalError(message=str(e)) from e


class RestaurantScheduleService:
	repository: RestaurantScheduleRepository
	restaurant_repository: RestaurantRepository

	def __init__(
		self, repository: RestaurantScheduleRepository, restaurant_repository: RestaurantRepository
	):
		self.repository = repository
		self.restaurant_repository = restaurant_repository

	async def create(
		self, restaurant_id: UUID, schedule: CreateRestaurantScheduleSchema
	) -> CreateRestaurantScheduleResponseSchema:
		try:
			restaurant = await self.restaurant_repository.get(restaurant_id)
			await self._validate_schedules_limit(restaurant.id)

			schedule_id = await self.repository.create(schedule, restaurant.id)
			logger.bind(created_restaurant_schedule_id=str(schedule_id))

			return CreateRestaurantScheduleResponseSchema(id=schedule_id)
		except RestaurantNotFoundError:
			raise
		except Exception as e:
			raise RestaurantSchedulesInternalError(message=str(e)) from e

	async def _validate_schedules_limit(self, restaurant_id: UUID) -> None:
		schedules = await self.repository.get_by_restaurant(restaurant_id)

		if len(schedules) >= 3:
			logger.warning(
				'Cannot create more than three active schedules for a restaurant',
				restaurant_id=str(restaurant_id),
				active_schedules_count=len(schedules),
			)
			raise RestaurantSchedulesInternalError(
				message='Cannot create more than three active schedules for a restaurant'
			)

	async def update(
		self,
		restaurant_id: UUID,
		schedule_id: UUID,
		schedule_update: UpdateRestaurantScheduleSchema,
	) -> RestaurantScheduleSchema:
		try:
			await self.restaurant_repository.get(restaurant_id)
			schedule = await self.repository.get(schedule_id)

			schedule.day_type = schedule_update.day_type.value
			schedule.start_day = schedule_update.start_day.value
			schedule.end_day = schedule_update.end_day.value
			schedule.start_time = datetime.strptime(schedule_update.start_time, '%H:%M:%S').time()
			schedule.end_time = datetime.strptime(schedule_update.end_time, '%H:%M:%S').time()

			await self.repository.update(schedule)
			logger.bind(updated_restaurant_schedule_id=schedule.id)

			return schedule
		except (RestaurantNotFoundError, RestaurantScheduleNotFoundError):
			raise
		except Exception as e:
			raise RestaurantSchedulesInternalError(message=str(e)) from e

	async def delete(self, restaurant_id: UUID, schedule_id: UUID) -> None:
		try:
			await self.restaurant_repository.get(restaurant_id)
			schedule = await self.repository.get(schedule_id)

			await self.repository.delete(schedule)
			logger.bind(deleted_restaurant_schedule_id=schedule_id)
		except (RestaurantNotFoundError, RestaurantScheduleNotFoundError):
			raise
		except Exception as e:
			raise RestaurantSchedulesInternalError(message=str(e)) from e
