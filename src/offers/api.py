from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .models import Offer, OfferSchedule
from .schemas import (
	OfferSchema,
	CreateOfferSchema,
	CreateOfferResponseSchema,
	UpdateOfferSchema,
	OfferScheduleSchema,
	CreateOfferScheduleSchema,
	CreateOfferScheduleResponseSchema,
	UpdateOfferScheduleSchema,
)
from core.deps import get_session

router = APIRouter()


# TODO: change all functions to list
@router.get(
	'/',
	name='Get offers',
	status_code=status.HTTP_200_OK,
	description='Get all offers',
	response_model=List[OfferSchema],
)
async def get_all_offers(db: AsyncSession = Depends(get_session)):
	async with db as session:
		try:
			result = await session.execute(select(Offer))
			offers: List[OfferSchema] = result.scalars().all()

			return offers
		except Exception as e:
			raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# TODO: change all functions to find
@router.get(
	'/{offer_id}',
	name='Get offer by ID',
	status_code=status.HTTP_200_OK,
	description='Get an offer by ID',
	response_model=OfferSchema,
)
async def get_offer(offer_id: str, db: AsyncSession = Depends(get_session)):
	async with db as session:
		try:
			result = await session.execute(select(Offer).where(Offer.id == offer_id))
			offer: OfferSchema = result.scalars().first()

			# TODO: return offer schedules here

			if not offer:
				raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Offer not found')

			return offer
		except Exception as e:
			raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post(
	'/',
	name='Create offer',
	status_code=status.HTTP_201_CREATED,
	description='Create a new offer',
	response_model=CreateOfferResponseSchema,
)
async def create_offer(offer: CreateOfferSchema, db: AsyncSession = Depends(get_session)):
	async with db as session:
		try:
			new_offer = Offer(**offer.model_dump())

			session.add(new_offer)
			await session.commit()

			return CreateOfferResponseSchema(id=new_offer.id)
		except Exception as e:
			raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.patch(
	'/{offer_id}',
	name='Update offer',
	status_code=status.HTTP_200_OK,
	description='Update an offer by id',
	response_model=OfferSchema,
)
async def update_offer(
	offer_id: str, body: UpdateOfferSchema, db: AsyncSession = Depends(get_session)
):
	async with db as session:
		try:
			result = await session.execute(select(Offer).where(Offer.id == offer_id))
			offer: Offer = result.scalars().first()

			if not offer:
				raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Offer not found')

			offer.price = body.price
			await session.commit()

			return offer
		except Exception as e:
			raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete(
	'/{offer_id}',
	name='Delete offer',
	status_code=status.HTTP_204_NO_CONTENT,
	description='Delete an offer by id',
)
async def delete_offer(offer_id: str, db: AsyncSession = Depends(get_session)):
	async with db as session:
		try:
			result = await session.execute(select(Offer).where(Offer.id == offer_id))
			offer: Offer = result.scalars().first()

			if not offer:
				raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Offer not found')

			await session.delete(offer)
			await session.commit()
		except Exception as e:
			raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# TODO: think about removing offer_id from url and pass it to request body (and restaurant schedules endpoints either)
@router.post(
	'/{offer_id}/schedules',
	name='Create offer schedule',
	status_code=status.HTTP_201_CREATED,
	description='Create a new offer schedule',
	response_model=CreateOfferScheduleResponseSchema,
)
async def create_offer_schedule(
	offer_id: str, schedule: CreateOfferScheduleSchema, db: AsyncSession = Depends(get_session)
):
	async with db as session:
		try:
			result = await session.execute(select(Offer).where(Offer.id == offer_id))
			offer: OfferSchema = result.scalars().first()

			# TODO: do not return offer schedules here

			if not offer:
				raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Offer not found')

			new_schedule = OfferSchedule(**schedule.model_dump())
			new_schedule.offer_id = offer_id
			new_schedule.start_time = datetime.strptime(schedule.start_time, '%H:%M:%S').time()
			new_schedule.end_time = datetime.strptime(schedule.end_time, '%H:%M:%S').time()

			session.add(new_schedule)
			await session.commit()

			return CreateOfferScheduleResponseSchema(id=new_schedule.id)
		except Exception as e:
			raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# TODO: must search offer schedules by offer_id and schedule_id? Or just schedule_id?
@router.patch(
	'/{offer_id}/schedules/{schedule_id}',
	name='Update offer schedule',
	status_code=status.HTTP_200_OK,
	description='Update an offer schedule by id',
	response_model=OfferScheduleSchema,
)
async def update_offer_schedule(
	offer_id: str,
	offer_schedule_id: str,
	body: UpdateOfferScheduleSchema,
	db: AsyncSession = Depends(get_session),
):
	async with db as session:
		try:
			result = await session.execute(select(Offer).where(Offer.id == offer_id))
			offer: Offer = result.scalars().first()

			if not offer:
				raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Offer not found')

			result = await session.execute(
				select(OfferSchedule).where(OfferSchedule.id == offer_schedule_id)
			)
			schedule: OfferSchedule = result.scalars().first()

			if not schedule:
				raise HTTPException(
					status_code=status.HTTP_404_NOT_FOUND, detail='Offer schedule not found'
				)

			schedule.day = body.day
			schedule.start_time = datetime.strptime(body.start_time, '%H:%M:%S').time()
			schedule.end_time = datetime.strptime(body.end_time, '%H:%M:%S').time()
			schedule.repeats = body.repeats

			return schedule
		except Exception as e:
			raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# TODO: pass only schedule_id
@router.delete(
	'/{offer_id}/schedules/{schedule_id}',
	name='Delete offer schedule',
	status_code=status.HTTP_204_NO_CONTENT,
	description='Delete an offer schedule by id',
)
async def delete_offer_schedule(
	offer_id: str, offer_schedule_id: str, db: AsyncSession = Depends(get_session)
):
	async with db as session:
		try:
			result = await session.execute(select(Offer).where(Offer.id == offer_id))
			offer: OfferSchema = result.scalars().first()

			if not offer:
				raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Offer not found')

			result = await session.execute(
				select(OfferSchedule).where(OfferSchedule.id == offer_schedule_id)
			)
			schedule: OfferSchedule = result.scalars().first()

			if not schedule:
				raise HTTPException(
					status_code=status.HTTP_404_NOT_FOUND, detail='Offer schedule not found'
				)

			await session.delete(offer)
			await session.commit()
		except Exception as e:
			raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
