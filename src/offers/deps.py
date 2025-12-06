from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.deps import get_session
from src.offers.repository import OfferRepository, OfferScheduleRepository
from src.offers.service import OfferScheduleService, OfferService


def get_offer_repository(
	db: AsyncSession = Depends(get_session),
) -> OfferRepository:
	return OfferRepository(db)


def get_offer_service(
	repository: OfferRepository = Depends(get_offer_repository),
) -> OfferService:
	return OfferService(repository)


OfferServiceDeps = Annotated[OfferService, Depends(get_offer_service)]


def get_offer_schedule_repository(
	db: AsyncSession = Depends(get_session),
) -> OfferScheduleRepository:
	return OfferScheduleRepository(db)


def get_offer_schedule_service(
	repository: OfferScheduleRepository = Depends(get_offer_schedule_repository),
	offer_repository: OfferRepository = Depends(get_offer_repository),
) -> OfferScheduleService:
	return OfferScheduleService(repository, offer_repository)


OfferScheduleServiceDeps = Annotated[
	OfferScheduleService,
	Depends(get_offer_schedule_service),
]
