from uuid import UUID

from fastapi import APIRouter, Query, status

from src.offers.deps import OfferScheduleServiceDeps, OfferServiceDeps
from src.offers.extended_schemas import OfferWithProductSchema
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

router = APIRouter()


@router.get(
	'',
	name='List offers',
	status_code=status.HTTP_200_OK,
	response_model=list[OfferWithProductSchema],
)
async def list_offers(service: OfferServiceDeps) -> list[OfferWithProductSchema]:
	return await service.list()


@router.get(
	'/active',
	name='List active offers near by',
	status_code=status.HTTP_200_OK,
	response_model=list[OfferWithProductSchema],
)
async def list_active_offers(
	service: OfferServiceDeps,
	latitude: float = Query(..., ge=-90, le=90, description='User latitude in decimal degrees'),
	longitude: float = Query(..., ge=-180, le=180, description='User longitude in decimal degrees'),
	radius: int = Query(
		default=10_000,
		gt=0,
		description='Search radius in meters (defaults to 10 km)',
	),
) -> list[OfferWithProductSchema]:
	return await service.list_active_near_by(latitude, longitude, radius)


@router.get(
	'/{id}',
	name='Find offer',
	status_code=status.HTTP_200_OK,
	response_model=OfferWithSchedulesSchema,
)
async def find_offer(id: UUID, service: OfferServiceDeps) -> OfferWithSchedulesSchema:
	return await service.get(id)


@router.post(
	'',
	name='Create offer',
	status_code=status.HTTP_201_CREATED,
	response_model=CreateOfferResponseSchema,
)
async def create_offer(
	body: CreateOfferSchema, service: OfferServiceDeps
) -> CreateOfferResponseSchema:
	return await service.create(body)


@router.patch(
	'/{id}',
	name='Update offer',
	status_code=status.HTTP_200_OK,
	response_model=OfferSchema,
)
async def update_offer(id: UUID, body: UpdateOfferSchema, service: OfferServiceDeps) -> OfferSchema:
	return await service.update(id, body)


@router.delete(
	'/{id}',
	name='Delete offer',
	status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_offer(id: UUID, service: OfferServiceDeps) -> None:
	await service.delete(id)


@router.post(
	'/{id}/schedules',
	name='Create offer schedule',
	status_code=status.HTTP_201_CREATED,
	response_model=CreateOfferScheduleResponseSchema,
)
async def create_offer_schedule(
	id: UUID,
	schedule: CreateOfferScheduleSchema,
	service: OfferScheduleServiceDeps,
) -> CreateOfferScheduleResponseSchema:
	return await service.create(id, schedule)


@router.patch(
	'/{id}/schedules/{schedule_id}',
	name='Update offer schedule',
	status_code=status.HTTP_200_OK,
	response_model=OfferScheduleSchema,
)
async def update_offer_schedule(
	id: UUID,
	schedule_id: UUID,
	body: UpdateOfferScheduleSchema,
	service: OfferScheduleServiceDeps,
) -> OfferScheduleSchema:
	return await service.update(id, schedule_id, body)


@router.delete(
	'/{id}/schedules/{schedule_id}',
	name='Delete offer schedule',
	status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_offer_schedule(
	id: UUID,
	schedule_id: UUID,
	service: OfferScheduleServiceDeps,
) -> None:
	await service.delete(id, schedule_id)
