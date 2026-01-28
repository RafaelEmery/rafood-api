from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.restaurants.exceptions import RestaurantNotFoundError, RestaurantScheduleNotFoundError
from src.restaurants.models import Restaurant, RestaurantSchedule
from src.restaurants.schemas import CreateRestaurantScheduleSchema, CreateRestaurantSchema


class RestaurantRepository:
	db: AsyncSession

	def __init__(self, db: AsyncSession):
		self.db = db

	async def list(self, name: str | None, owner_id: UUID | None) -> list[Restaurant]:
		query = select(Restaurant)

		if name is not None:
			query = query.filter(Restaurant.name.contains(name))
		if owner_id is not None:
			query = query.filter(Restaurant.owner_id == owner_id)

		result = await self.db.execute(query)

		return result.scalars().unique().all()

	async def get(self, id: UUID) -> Restaurant:
		result = await self.db.execute(select(Restaurant).where(Restaurant.id == id))
		restaurant = result.scalars().unique().first()

		if not restaurant:
			raise RestaurantNotFoundError(restaurant_id=str(id))

		return restaurant

	async def create(self, restaurant: CreateRestaurantSchema) -> UUID:
		new_restaurant = Restaurant(**restaurant.model_dump())

		self.db.add(new_restaurant)
		await self.db.commit()

		return new_restaurant.id

	async def update(self, restaurant: Restaurant) -> None:
		self.db.add(restaurant)

		await self.db.commit()
		await self.db.refresh(restaurant)

	async def delete(self, restaurant: Restaurant) -> None:
		await self.db.delete(restaurant)
		await self.db.commit()


class RestaurantScheduleRepository:
	db: AsyncSession

	def __init__(self, db: AsyncSession):
		self.db = db

	async def create(self, schedule: CreateRestaurantScheduleSchema, restaurant_id: UUID) -> UUID:
		new_schedule = RestaurantSchedule(**schedule.model_dump())
		new_schedule.restaurant_id = restaurant_id
		new_schedule.start_time = datetime.strptime(schedule.start_time, '%H:%M:%S').time()
		new_schedule.end_time = datetime.strptime(schedule.end_time, '%H:%M:%S').time()
		new_schedule.day_type = schedule.day_type.value
		new_schedule.start_day = schedule.start_day.value
		new_schedule.end_day = schedule.end_day.value

		self.db.add(new_schedule)
		await self.db.commit()

		return new_schedule.id

	async def get(self, schedule_id: UUID) -> RestaurantSchedule:
		result = await self.db.execute(
			select(RestaurantSchedule).where(RestaurantSchedule.id == schedule_id)
		)
		schedule = result.scalars().unique().first()

		if not schedule:
			raise RestaurantScheduleNotFoundError(schedule_id=str(schedule_id))

		return schedule

	async def update(self, schedule: RestaurantSchedule) -> None:
		self.db.add(schedule)

		await self.db.commit()
		await self.db.refresh(schedule)

	async def get_by_restaurant(self, restaurant_id: UUID) -> list[RestaurantSchedule]:
		result = await self.db.execute(
			select(RestaurantSchedule).where(
				RestaurantSchedule.restaurant_id == restaurant_id,
			)
		)

		return result.scalars().unique().all()

	async def delete(self, schedule: RestaurantSchedule) -> None:
		await self.db.delete(schedule)
		await self.db.commit()
