from datetime import datetime
from uuid import UUID

from src.core.logging.logger import StructLogger
from src.offers.exceptions import (
	OfferNotFoundError,
	OfferScheduleNotFoundError,
	OfferSchedulesInternalError,
	OffersInternalError,
)
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

logger = StructLogger()


class OfferService:
	repository: OfferRepository

	def __init__(self, repository: OfferRepository):
		self.repository = repository

	async def list(self) -> list[OfferSchema]:
		try:
			offers = await self.repository.list()
			logger.bind(listed_offers_count=len(offers))

			return offers
		except Exception as e:
			raise OffersInternalError(message=str(e)) from e

	async def get(self, id: UUID) -> OfferWithSchedulesSchema:
		try:
			offer = await self.repository.get(id)
			logger.bind(retrieved_offer_id=offer.id)

			return offer
		except OfferNotFoundError:
			raise
		except Exception as e:
			raise OffersInternalError(message=str(e)) from e

	async def create(self, offer: CreateOfferSchema) -> CreateOfferResponseSchema:
		try:
			offer_id = await self.repository.create(offer)
			logger.bind(created_offer_id=str(offer_id))

			return CreateOfferResponseSchema(id=offer_id)
		except Exception as e:
			raise OffersInternalError(message=str(e)) from e

	async def update(self, id: UUID, offer_update: UpdateOfferSchema) -> OfferSchema:
		try:
			offer = await self.repository.get(id)

			offer.price = offer_update.price
			offer.active = offer_update.active
			await self.repository.update(offer)
			logger.bind(updated_offer_id=offer.id)

			return offer
		except OfferNotFoundError:
			raise
		except Exception as e:
			raise OffersInternalError(message=str(e)) from e

	async def delete(self, id: UUID) -> None:
		try:
			offer = await self.repository.get(id)

			await self.repository.delete(offer)
			logger.bind(deleted_offer_id=id)
		except OfferNotFoundError:
			raise
		except Exception as e:
			raise OffersInternalError(message=str(e)) from e


class OfferScheduleService:
	repository: OfferScheduleRepository
	offer_repository: OfferRepository

	def __init__(self, repository: OfferScheduleRepository, offer_repository: OfferRepository):
		self.repository = repository
		self.offer_repository = offer_repository

	async def create(
		self, offer_id: UUID, schedule: CreateOfferScheduleSchema
	) -> CreateOfferScheduleResponseSchema:
		try:
			offer = await self.offer_repository.get(offer_id)
			schedule_id = await self.repository.create(schedule, offer.id)
			logger.bind(created_offer_schedule_id=str(schedule_id))

			return CreateOfferScheduleResponseSchema(id=schedule_id)
		except OfferNotFoundError:
			raise
		except Exception as e:
			raise OfferSchedulesInternalError(message=str(e)) from e

	async def update(
		self, offer_id: UUID, schedule_id: UUID, schedule_update: UpdateOfferScheduleSchema
	) -> OfferScheduleSchema:
		try:
			await self.offer_repository.get(offer_id)
			schedule = await self.repository.get(schedule_id)

			schedule.day = schedule_update.day.value
			schedule.start_time = datetime.strptime(schedule_update.start_time, '%H:%M:%S').time()
			schedule.end_time = datetime.strptime(schedule_update.end_time, '%H:%M:%S').time()
			schedule.repeats = schedule_update.repeats
			await self.repository.update(schedule)
			logger.bind(updated_offer_schedule_id=schedule.id)

			return schedule
		except (OfferNotFoundError, OfferScheduleNotFoundError):
			raise
		except Exception as e:
			raise OfferSchedulesInternalError(message=str(e)) from e

	async def delete(self, offer_id: UUID, schedule_id: UUID) -> None:
		try:
			await self.offer_repository.get(offer_id)
			schedule = await self.repository.get(schedule_id)

			await self.repository.delete(schedule)
			logger.bind(deleted_offer_schedule_id=schedule.id)
		except (OfferNotFoundError, OfferScheduleNotFoundError):
			raise
		except Exception as e:
			raise OfferSchedulesInternalError(message=str(e)) from e
