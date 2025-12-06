from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import OfferNotFoundError, OfferScheduleNotFoundError
from src.offers.models import Offer, OfferSchedule
from src.offers.schemas import CreateOfferScheduleSchema, CreateOfferSchema


class OfferRepository:
	db: AsyncSession

	def __init__(self, db: AsyncSession):
		self.db = db

	async def list(self) -> list[Offer]:
		result = await self.db.execute(select(Offer))

		return result.scalars().unique().all()

	async def get(self, id: UUID) -> Offer:
		result = await self.db.execute(select(Offer).where(Offer.id == id))
		offer = result.scalars().unique().first()

		if not offer:
			raise OfferNotFoundError('Offer not found')

		return offer

	async def create(self, offer: CreateOfferSchema) -> UUID:
		new_offer = Offer(**offer.model_dump())

		self.db.add(new_offer)
		await self.db.commit()

		return new_offer.id

	async def update(self, offer: Offer) -> Offer:
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
		result = await self.db.execute(select(OfferSchedule).where(OfferSchedule.id == schedule_id))
		schedule = result.scalars().unique().first()

		if not schedule:
			raise OfferScheduleNotFoundError('Offer schedule not found')

		return schedule

	async def update(self, schedule: OfferSchedule) -> None:
		self.db.add(schedule)

		await self.db.commit()
		await self.db.refresh(schedule)

	async def delete(self, schedule: OfferSchedule) -> None:
		await self.db.delete(schedule)
		await self.db.commit()
