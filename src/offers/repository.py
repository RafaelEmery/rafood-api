from datetime import datetime
from uuid import UUID

from sqlalchemy import exists, select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.schedule_matching import current_day_name, schedule_time_in_range
from src.offers.exceptions import OfferNotFoundError, OfferScheduleNotFoundError
from src.offers.models import Offer, OfferSchedule
from src.offers.schemas import CreateOfferScheduleSchema, CreateOfferSchema
from src.products.models import Product
from src.restaurants.models import Restaurant


class OfferRepository:
	db: AsyncSession

	def __init__(self, db: AsyncSession):
		self.db = db

	def _active_schedule_exists(self, reference_time: datetime) -> exists:  # type: ignore[valid-type]
		"""
		Check if the offer has an active schedule with the current day and time.

		Consider the offer schedule to check if the offer is active
		with the current day and time.
		"""
		return exists(
			select(1).where(
				OfferSchedule.offer_id == Offer.id,  # type: ignore[arg-type]
				OfferSchedule.day == current_day_name(reference_time),  # type: ignore[arg-type]
				schedule_time_in_range(
					OfferSchedule.start_time,
					OfferSchedule.end_time,
					reference_time,
				),  # type: ignore[arg-type]
			)
		)

	async def list_active_near_by(
		self,
		latitude: float,
		longitude: float,
		radius_meters: int,
	) -> list[Offer]:
		"""
		List active offers nearby the location using PostGIS ST_DWithin function
		and the GiST index on restaurants geography expression.

		Location is resolved via Offer → Product → Restaurant. Only offers marked
		active with a matching schedule for the current day and time are returned.

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
			select(Offer)
			.options(selectinload(Offer.product))  # type: ignore[arg-type]
			.join(Product, Offer.product_id == Product.id)  # type: ignore[arg-type]
			.join(Restaurant, Product.restaurant_id == Restaurant.id)  # type: ignore[arg-type]
			.where(Offer.active.is_(True))  # type: ignore[attr-defined]
			.where(spatial_filter)
			.where(self._active_schedule_exists(datetime.now()))
		)
		result = await self.db.execute(query)

		return list(result.scalars().unique().all())

	async def list(self) -> list[Offer]:
		query = select(Offer).options(selectinload(Offer.product))  # type: ignore[arg-type]
		result = await self.db.execute(query)

		return list(result.scalars().unique().all())

	async def get(self, id: UUID) -> Offer:
		result = await self.db.execute(select(Offer).where(Offer.id == id))  # type: ignore[arg-type]
		offer = result.scalars().unique().first()

		if not offer:
			raise OfferNotFoundError(offer_id=str(id))

		return offer

	async def create(self, offer: CreateOfferSchema) -> UUID:
		new_offer = Offer(**offer.model_dump())

		self.db.add(new_offer)
		await self.db.commit()

		return new_offer.id

	async def update(self, offer: Offer) -> None:
		self.db.add(offer)

		await self.db.commit()
		await self.db.refresh(offer)

	async def delete(self, offer: Offer) -> None:
		await self.db.delete(offer)
		await self.db.commit()


class OfferScheduleRepository:
	db: AsyncSession

	def __init__(self, db: AsyncSession):
		self.db = db

	async def create(self, schedule: CreateOfferScheduleSchema, offer_id: UUID) -> UUID:
		new_schedule = OfferSchedule(**schedule.model_dump())
		new_schedule.offer_id = offer_id
		new_schedule.day = schedule.day.value
		new_schedule.start_time = datetime.strptime(schedule.start_time, '%H:%M:%S').time()
		new_schedule.end_time = datetime.strptime(schedule.end_time, '%H:%M:%S').time()

		self.db.add(new_schedule)
		await self.db.commit()

		return new_schedule.id

	async def get(self, schedule_id: UUID) -> OfferSchedule:
		result = await self.db.execute(select(OfferSchedule).where(OfferSchedule.id == schedule_id))  # type: ignore[arg-type]
		schedule = result.scalars().unique().first()

		if not schedule:
			raise OfferScheduleNotFoundError(schedule_id=str(schedule_id))

		return schedule

	async def update(self, schedule: OfferSchedule) -> None:
		self.db.add(schedule)

		await self.db.commit()
		await self.db.refresh(schedule)

	async def delete(self, schedule: OfferSchedule) -> None:
		await self.db.delete(schedule)
		await self.db.commit()
