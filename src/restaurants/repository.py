from datetime import datetime
from uuid import UUID

from sqlalchemy import exists, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.schedule_matching import (
	current_day_type,
	day_in_range,
	schedule_time_in_range,
)
from src.enums import DayType
from src.restaurants.exceptions import RestaurantNotFoundError, RestaurantScheduleNotFoundError
from src.restaurants.models import Restaurant, RestaurantSchedule
from src.restaurants.schemas import CreateRestaurantScheduleSchema, CreateRestaurantSchema


class RestaurantRepository:
	db: AsyncSession

	def __init__(self, db: AsyncSession):
		self.db = db

	def _open_schedule_exists(self, reference_time: datetime) -> exists:  # type: ignore[valid-type]
		"""
		Check if the restaurant is open with the current day and time.

		Consider the restaurant schedule to check if the restaurant is open
		with the current day and time.
		"""
		return exists(
			select(1).where(
				RestaurantSchedule.restaurant_id == Restaurant.id,  # type: ignore[arg-type]
				RestaurantSchedule.day_type != DayType.HOLIDAY.value,  # type: ignore[arg-type]
				RestaurantSchedule.day_type == current_day_type(reference_time),  # type: ignore[arg-type]
				day_in_range(
					RestaurantSchedule.start_day,
					RestaurantSchedule.end_day,
					reference_time,
				),  # type: ignore[arg-type]
				schedule_time_in_range(
					RestaurantSchedule.start_time,
					RestaurantSchedule.end_time,
					reference_time,
				),  # type: ignore[arg-type]
			)
		)

	async def list_open_near_by(
		self,
		latitude: float,
		longitude: float,
		radius_meters: int,
	) -> list[Restaurant]:
		"""
		List open restaurants nearby the location using PostGIS ST_DWithin function
		and the GiST index on restaurants geography expression.

		Consider the restaurant schedule to check if the restaurant is open
		with the current day and time.

		ST_DWithin is a function that checks if a point is within a given distance of another point.
		geography is a function that converts a point to a geography type.
		ST_SetSRID is a function that sets the SRID of a point (SRID is Spatial Reference Identifier).
		ST_MakePoint is a function that makes a point from a longitude and latitude.
		restaurants.longitude and restaurants.latitude are the longitude and latitude of the restaurant.
		longitude and latitude are the longitude and latitude of the location to check.
		radius is the radius in meters to check.

		Extra: 4326 is the SRID for the Earth's surface in the World Geodetic System 1984 coordinate system.
		"""
		spatial_filter = text(
			"""
			ST_DWithin(
				geography(ST_SetSRID(ST_MakePoint(restaurants.longitude, restaurants.latitude), 4326)),
				geography(ST_SetSRID(ST_MakePoint(:longitude, :latitude), 4326)),
				:radius
			)
			"""
		).bindparams(longitude=longitude, latitude=latitude, radius=radius_meters)

		query = (
			select(Restaurant)
			.where(spatial_filter)
			.where(self._open_schedule_exists(datetime.now()))
		)
		result = await self.db.execute(query)
		restaurants: list[Restaurant] = list(result.scalars().unique().all())

		return restaurants

	async def list(self, name: str | None, owner_id: UUID | None) -> list[Restaurant]:
		query = select(Restaurant)

		if name is not None:
			query = query.filter(Restaurant.name.contains(name))  # type: ignore[attr-defined]
		if owner_id is not None:
			query = query.filter(Restaurant.owner_id == owner_id)  # type: ignore[arg-type]

		result = await self.db.execute(query)
		restaurants: list[Restaurant] = list(result.scalars().unique().all())

		return restaurants

	async def get(self, id: UUID) -> Restaurant:
		result = await self.db.execute(select(Restaurant).where(Restaurant.id == id))  # type: ignore[arg-type]
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
			select(RestaurantSchedule).where(RestaurantSchedule.id == schedule_id)  # type: ignore[arg-type]
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
				RestaurantSchedule.restaurant_id == restaurant_id,  # type: ignore[arg-type]
			)
		)

		return list(result.scalars().unique().all())

	async def delete(self, schedule: RestaurantSchedule) -> None:
		await self.db.delete(schedule)
		await self.db.commit()
