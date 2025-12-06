from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from src.exceptions import OfferNotFoundError, OfferScheduleNotFoundError
from src.offers.deps import OfferScheduleServiceDeps, OfferServiceDeps
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
	response_model=list[OfferSchema],
)
async def list_offers(service: OfferServiceDeps):
	try:
		return await service.list()
	except Exception as e:
		raise HTTPException(500, str(e)) from e


@router.get(
	'/{id}',
	name='Find offer',
	status_code=status.HTTP_200_OK,
	response_model=OfferWithSchedulesSchema,
)
async def find_offer(id: UUID, service: OfferServiceDeps):
	try:
		return await service.get(id)
	except OfferNotFoundError as e:
		raise HTTPException(status.HTTP_404_NOT_FOUND, str(e)) from e
	except Exception as e:
		raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e)) from e


@router.post(
	'',
	name='Create offer',
	status_code=status.HTTP_201_CREATED,
	response_model=CreateOfferResponseSchema,
)
async def create_offer(body: CreateOfferSchema, service: OfferServiceDeps):
	try:
		return await service.create(body)
	except Exception as e:
		raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e)) from e


@router.patch(
	'/{id}',
	name='Update offer',
	status_code=status.HTTP_200_OK,
	response_model=OfferSchema,
)
async def update_offer(id: UUID, body: UpdateOfferSchema, service: OfferServiceDeps):
	try:
		return await service.update(id, body)
	except OfferNotFoundError as e:
		raise HTTPException(status.HTTP_404_NOT_FOUND, str(e)) from e
	except Exception as e:
		raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e)) from e


@router.delete(
	'/{id}',
	name='Delete offer',
	status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_offer(id: UUID, service: OfferServiceDeps):
	try:
		await service.delete(id)
	except OfferNotFoundError as e:
		raise HTTPException(status.HTTP_404_NOT_FOUND, str(e)) from e
	except Exception as e:
		raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e)) from e


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
):
	try:
		return await service.create(id, schedule)
	except OfferNotFoundError as e:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


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
):
	try:
		return await service.update(id, schedule_id, body)
	except OfferNotFoundError as e:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
	except OfferScheduleNotFoundError as e:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.delete(
	'/{id}/schedules/{schedule_id}',
	name='Delete offer schedule',
	status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_offer_schedule(
	id: UUID,
	schedule_id: UUID,
	service: OfferScheduleServiceDeps,
):
	try:
		await service.delete(id, schedule_id)
	except OfferNotFoundError as e:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
	except OfferScheduleNotFoundError as e:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e
