from datetime import time
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.offers.exceptions import (
	OfferNotFoundError,
	OfferScheduleNotFoundError,
	OfferSchedulesInternalError,
	OffersInternalError,
)
from src.offers.schemas import (
	CreateOfferScheduleSchema,
	CreateOfferSchema,
	UpdateOfferScheduleSchema,
	UpdateOfferSchema,
)


@pytest.mark.asyncio
async def test_list_offers_success(offer_service, mock_offer_repository, sample_offer):
	mock_offer_repository.list = AsyncMock(return_value=[sample_offer])

	result = await offer_service.list()

	assert len(result) == 1
	assert result[0].id == sample_offer.id

	mock_offer_repository.list.assert_awaited_once()


@pytest.mark.asyncio
async def test_list_offers_internal_error(offer_service, mock_offer_repository):
	mock_offer_repository.list = AsyncMock(side_effect=Exception('Ih! Deu ruim!'))

	with pytest.raises(OffersInternalError) as exc_info:
		await offer_service.list()

	assert 'Ih! Deu ruim!' in str(exc_info.value)

	mock_offer_repository.list.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_offer_success(offer_service, mock_offer_repository, sample_offer_with_schedules):
	mock_offer_repository.get = AsyncMock(return_value=sample_offer_with_schedules)

	result = await offer_service.get(id=sample_offer_with_schedules.id)

	assert result.id == sample_offer_with_schedules.id
	assert result.price == sample_offer_with_schedules.price

	mock_offer_repository.get.assert_awaited_once_with(sample_offer_with_schedules.id)


@pytest.mark.asyncio
async def test_get_offer_not_found(offer_service, mock_offer_repository):
	offer_id = uuid4()
	mock_offer_repository.get = AsyncMock(side_effect=OfferNotFoundError(offer_id=str(offer_id)))

	with pytest.raises(OfferNotFoundError):
		await offer_service.get(id=offer_id)

	mock_offer_repository.get.assert_awaited_once_with(offer_id)


@pytest.mark.asyncio
async def test_get_offer_internal_error(offer_service, mock_offer_repository):
	offer_id = uuid4()
	mock_offer_repository.get = AsyncMock(side_effect=Exception('Ih! Deu ruim!'))

	with pytest.raises(OffersInternalError) as exc_info:
		await offer_service.get(id=offer_id)

	assert 'Ih! Deu ruim!' in str(exc_info.value)

	mock_offer_repository.get.assert_awaited_once_with(offer_id)


@pytest.mark.asyncio
async def test_create_offer_success(offer_service, mock_offer_repository):
	offer_id = uuid4()
	create_data = CreateOfferSchema(
		product_id=uuid4(),
		price=10.0,
		active=True,
	)
	mock_offer_repository.create = AsyncMock(return_value=offer_id)

	result = await offer_service.create(offer=create_data)

	assert result.id == offer_id

	mock_offer_repository.create.assert_awaited_once_with(create_data)


@pytest.mark.asyncio
async def test_create_offer_internal_error(offer_service, mock_offer_repository):
	create_data = CreateOfferSchema(
		product_id=uuid4(),
		price=10.0,
		active=True,
	)
	mock_offer_repository.create = AsyncMock(side_effect=Exception('Ih! Deu ruim!'))

	with pytest.raises(OffersInternalError) as exc_info:
		await offer_service.create(offer=create_data)

	assert 'Ih! Deu ruim!' in str(exc_info.value)

	mock_offer_repository.create.assert_awaited_once_with(create_data)


@pytest.mark.asyncio
async def test_update_offer_success(offer_service, mock_offer_repository, sample_offer):
	update_data = UpdateOfferSchema(
		price=20.0,
		active=False,
	)
	mock_offer_repository.get = AsyncMock(return_value=sample_offer)
	mock_offer_repository.update = AsyncMock()

	result = await offer_service.update(id=sample_offer.id, offer_update=update_data)

	assert result.price == 20.0
	assert result.active is False

	mock_offer_repository.get.assert_awaited_once_with(sample_offer.id)
	mock_offer_repository.update.assert_awaited_once_with(sample_offer)


@pytest.mark.asyncio
async def test_update_offer_not_found(offer_service, mock_offer_repository):
	offer_id = uuid4()
	update_data = UpdateOfferSchema(
		price=20.0,
		active=False,
	)
	mock_offer_repository.get = AsyncMock(side_effect=OfferNotFoundError(offer_id=str(offer_id)))

	with pytest.raises(OfferNotFoundError):
		await offer_service.update(id=offer_id, offer_update=update_data)

	mock_offer_repository.get.assert_awaited_once_with(offer_id)


@pytest.mark.asyncio
async def test_update_offer_internal_error(offer_service, mock_offer_repository, sample_offer):
	update_data = UpdateOfferSchema(
		price=20.0,
		active=False,
	)
	mock_offer_repository.get = AsyncMock(return_value=sample_offer)
	mock_offer_repository.update = AsyncMock(side_effect=Exception('Ih! Deu ruim!'))

	with pytest.raises(OffersInternalError) as exc_info:
		await offer_service.update(id=sample_offer.id, offer_update=update_data)

	assert 'Ih! Deu ruim!' in str(exc_info.value)


@pytest.mark.asyncio
async def test_delete_offer_success(offer_service, mock_offer_repository, sample_offer):
	mock_offer_repository.get = AsyncMock(return_value=sample_offer)
	mock_offer_repository.delete = AsyncMock()

	await offer_service.delete(id=sample_offer.id)

	mock_offer_repository.get.assert_awaited_once_with(sample_offer.id)
	mock_offer_repository.delete.assert_awaited_once_with(sample_offer)


@pytest.mark.asyncio
async def test_delete_offer_not_found(offer_service, mock_offer_repository):
	offer_id = uuid4()
	mock_offer_repository.get = AsyncMock(side_effect=OfferNotFoundError(offer_id=str(offer_id)))

	with pytest.raises(OfferNotFoundError):
		await offer_service.delete(id=offer_id)

	mock_offer_repository.get.assert_awaited_once_with(offer_id)


@pytest.mark.asyncio
async def test_delete_offer_internal_error(offer_service, mock_offer_repository, sample_offer):
	mock_offer_repository.get = AsyncMock(return_value=sample_offer)
	mock_offer_repository.delete = AsyncMock(side_effect=Exception('Ih! Deu ruim!'))

	with pytest.raises(OffersInternalError) as exc_info:
		await offer_service.delete(id=sample_offer.id)

	assert 'Ih! Deu ruim!' in str(exc_info.value)


@pytest.mark.asyncio
async def test_create_offer_schedule_success(
	schedule_service, mock_schedule_repository, mock_offer_repository, sample_offer
):
	schedule_id = uuid4()
	create_data = CreateOfferScheduleSchema(
		day='monday',
		start_time='08:00:00',
		end_time='18:00:00',
		repeats=False,
	)
	mock_offer_repository.get = AsyncMock(return_value=sample_offer)
	mock_schedule_repository.create = AsyncMock(return_value=schedule_id)

	result = await schedule_service.create(offer_id=sample_offer.id, schedule=create_data)

	assert result.id == schedule_id

	mock_offer_repository.get.assert_awaited_once_with(sample_offer.id)
	mock_schedule_repository.create.assert_awaited_once_with(create_data, sample_offer.id)


@pytest.mark.asyncio
async def test_create_offer_schedule_offer_not_found(schedule_service, mock_offer_repository):
	offer_id = uuid4()
	create_data = CreateOfferScheduleSchema(
		day='monday',
		start_time='08:00:00',
		end_time='18:00:00',
		repeats=False,
	)
	mock_offer_repository.get = AsyncMock(side_effect=OfferNotFoundError(offer_id=str(offer_id)))

	with pytest.raises(OfferNotFoundError):
		await schedule_service.create(offer_id=offer_id, schedule=create_data)

	mock_offer_repository.get.assert_awaited_once_with(offer_id)


@pytest.mark.asyncio
async def test_create_offer_schedule_internal_error(
	schedule_service, mock_schedule_repository, mock_offer_repository, sample_offer
):
	create_data = CreateOfferScheduleSchema(
		day='monday',
		start_time='08:00:00',
		end_time='18:00:00',
		repeats=False,
	)
	mock_offer_repository.get = AsyncMock(return_value=sample_offer)
	mock_schedule_repository.create = AsyncMock(side_effect=Exception('Ih! Deu ruim!'))

	with pytest.raises(OfferSchedulesInternalError) as exc_info:
		await schedule_service.create(offer_id=sample_offer.id, schedule=create_data)

	assert 'Ih! Deu ruim!' in str(exc_info.value)


@pytest.mark.asyncio
async def test_update_offer_schedule_success(
	schedule_service,
	mock_schedule_repository,
	mock_offer_repository,
	sample_offer,
	sample_schedule,
):
	update_data = UpdateOfferScheduleSchema(
		day='tuesday',
		start_time='10:00:00',
		end_time='22:00:00',
		repeats=True,
	)
	mock_offer_repository.get = AsyncMock(return_value=sample_offer)
	mock_schedule_repository.get = AsyncMock(return_value=sample_schedule)
	mock_schedule_repository.update = AsyncMock()

	result = await schedule_service.update(
		offer_id=sample_offer.id,
		schedule_id=sample_schedule.id,
		schedule_update=update_data,
	)

	assert result.day == 'tuesday'
	assert result.start_time == time(10, 0, 0)
	assert result.end_time == time(22, 0, 0)
	assert result.repeats is True

	mock_offer_repository.get.assert_awaited_once_with(sample_offer.id)
	mock_schedule_repository.get.assert_awaited_once_with(sample_schedule.id)
	mock_schedule_repository.update.assert_awaited_once_with(sample_schedule)


@pytest.mark.asyncio
async def test_update_offer_schedule_offer_not_found(schedule_service, mock_offer_repository):
	offer_id = uuid4()
	schedule_id = uuid4()
	update_data = UpdateOfferScheduleSchema(
		day='tuesday',
		start_time='10:00:00',
		end_time='22:00:00',
		repeats=True,
	)
	mock_offer_repository.get = AsyncMock(side_effect=OfferNotFoundError(offer_id=str(offer_id)))

	with pytest.raises(OfferNotFoundError):
		await schedule_service.update(
			offer_id=offer_id, schedule_id=schedule_id, schedule_update=update_data
		)

	mock_offer_repository.get.assert_awaited_once_with(offer_id)


@pytest.mark.asyncio
async def test_update_offer_schedule_not_found(
	schedule_service, mock_schedule_repository, mock_offer_repository, sample_offer
):
	schedule_id = uuid4()
	update_data = UpdateOfferScheduleSchema(
		day='tuesday',
		start_time='10:00:00',
		end_time='22:00:00',
		repeats=True,
	)
	mock_offer_repository.get = AsyncMock(return_value=sample_offer)
	mock_schedule_repository.get = AsyncMock(
		side_effect=OfferScheduleNotFoundError(schedule_id=str(schedule_id))
	)

	with pytest.raises(OfferScheduleNotFoundError):
		await schedule_service.update(
			offer_id=sample_offer.id, schedule_id=schedule_id, schedule_update=update_data
		)

	mock_offer_repository.get.assert_awaited_once_with(sample_offer.id)
	mock_schedule_repository.get.assert_awaited_once_with(schedule_id)


@pytest.mark.asyncio
async def test_update_offer_schedule_internal_error(
	schedule_service,
	mock_schedule_repository,
	mock_offer_repository,
	sample_offer,
	sample_schedule,
):
	update_data = UpdateOfferScheduleSchema(
		day='tuesday',
		start_time='10:00:00',
		end_time='22:00:00',
		repeats=True,
	)
	mock_offer_repository.get = AsyncMock(return_value=sample_offer)
	mock_schedule_repository.get = AsyncMock(return_value=sample_schedule)
	mock_schedule_repository.update = AsyncMock(side_effect=Exception('Ih! Deu ruim!'))

	with pytest.raises(OfferSchedulesInternalError) as exc_info:
		await schedule_service.update(
			offer_id=sample_offer.id,
			schedule_id=sample_schedule.id,
			schedule_update=update_data,
		)

	assert 'Ih! Deu ruim!' in str(exc_info.value)


@pytest.mark.asyncio
async def test_delete_offer_schedule_success(
	schedule_service,
	mock_schedule_repository,
	mock_offer_repository,
	sample_offer,
	sample_schedule,
):
	mock_offer_repository.get = AsyncMock(return_value=sample_offer)
	mock_schedule_repository.get = AsyncMock(return_value=sample_schedule)
	mock_schedule_repository.delete = AsyncMock()

	await schedule_service.delete(offer_id=sample_offer.id, schedule_id=sample_schedule.id)

	mock_offer_repository.get.assert_awaited_once_with(sample_offer.id)
	mock_schedule_repository.get.assert_awaited_once_with(sample_schedule.id)
	mock_schedule_repository.delete.assert_awaited_once_with(sample_schedule)


@pytest.mark.asyncio
async def test_delete_offer_schedule_offer_not_found(schedule_service, mock_offer_repository):
	offer_id = uuid4()
	schedule_id = uuid4()
	mock_offer_repository.get = AsyncMock(side_effect=OfferNotFoundError(offer_id=str(offer_id)))

	with pytest.raises(OfferNotFoundError):
		await schedule_service.delete(offer_id=offer_id, schedule_id=schedule_id)

	mock_offer_repository.get.assert_awaited_once_with(offer_id)


@pytest.mark.asyncio
async def test_delete_offer_schedule_not_found(
	schedule_service, mock_schedule_repository, mock_offer_repository, sample_offer
):
	schedule_id = uuid4()
	mock_offer_repository.get = AsyncMock(return_value=sample_offer)
	mock_schedule_repository.get = AsyncMock(
		side_effect=OfferScheduleNotFoundError(schedule_id=str(schedule_id))
	)

	with pytest.raises(OfferScheduleNotFoundError):
		await schedule_service.delete(offer_id=sample_offer.id, schedule_id=schedule_id)

	mock_offer_repository.get.assert_awaited_once_with(sample_offer.id)
	mock_schedule_repository.get.assert_awaited_once_with(schedule_id)


@pytest.mark.asyncio
async def test_delete_offer_schedule_internal_error(
	schedule_service,
	mock_schedule_repository,
	mock_offer_repository,
	sample_offer,
	sample_schedule,
):
	mock_offer_repository.get = AsyncMock(return_value=sample_offer)
	mock_schedule_repository.get = AsyncMock(return_value=sample_schedule)
	mock_schedule_repository.delete = AsyncMock(side_effect=Exception('Ih! Deu ruim!'))

	with pytest.raises(OfferSchedulesInternalError) as exc_info:
		await schedule_service.delete(offer_id=sample_offer.id, schedule_id=sample_schedule.id)

	assert 'Ih! Deu ruim!' in str(exc_info.value)
