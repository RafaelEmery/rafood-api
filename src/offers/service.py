from datetime import datetime
from uuid import UUID

from src.offers.repository import OfferRepository, OfferScheduleRepository
from src.offers.schemas import (
	CreateOfferResponseSchema,
	CreateOfferScheduleResponseSchema,
	CreateOfferScheduleSchema,
	CreateOfferSchema,
	OfferScheduleSchema,
	OfferSchema,
	OfferWithSchedulesSchema,
	UpdateOfferScheduleSchema,
	UpdateOfferSchema,
)


class OfferService:
	repository: OfferRepository

	def __init__(self, repository: OfferRepository):
		self.repository = repository

	async def list(self) -> list[OfferSchema]:
		return await self.repository.list()

	async def get(self, id: UUID) -> OfferWithSchedulesSchema:
		return await self.repository.get(id)

	async def create(self, offer: CreateOfferSchema) -> CreateOfferResponseSchema:
		offer_id = await self.repository.create(offer)

		return CreateOfferResponseSchema(id=offer_id)

	async def update(self, id: UUID, offer_update: UpdateOfferSchema) -> OfferSchema:
		offer = await self.repository.get(id)

		offer.price = offer_update.price
		await self.repository.update(offer)

		return offer

	async def delete(self, id: UUID) -> None:
		offer = await self.repository.get(id)

		await self.repository.delete(offer)


class OfferScheduleService:
	repository: OfferScheduleRepository
	offer_repository: OfferRepository

	def __init__(self, repository, offer_repository):
		self.repository = repository
		self.offer_repository = offer_repository

	async def create(self, offer_id: UUID, schedule: CreateOfferScheduleSchema):
		offer = await self.offer_repository.get(offer_id)
		schedule_id = await self.repository.create(schedule, offer.id)

		return CreateOfferScheduleResponseSchema(id=schedule_id)

	async def update(
		self, offer_id: UUID, schedule_id: UUID, schedule_update: UpdateOfferScheduleSchema
	) -> OfferScheduleSchema:
		await self.offer_repository.get(offer_id)
		schedule = await self.repository.get(schedule_id)

		schedule.day = schedule_update.day.value
		schedule.start_time = datetime.strptime(schedule_update.start_time, '%H:%M:%S').time()
		schedule.end_time = datetime.strptime(schedule_update.end_time, '%H:%M:%S').time()
		schedule.repeats = schedule_update.repeats
		await self.repository.update(schedule)

		return schedule

	async def delete(self, offer_id: UUID, schedule_id: UUID):
		await self.offer_repository.get(offer_id)
		schedule = await self.repository.get(schedule_id)

		await self.repository.delete(schedule)
