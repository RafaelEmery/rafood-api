from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.enums import Day, DayType
from src.restaurants.exceptions import (
	RestaurantNotFoundError,
	RestaurantScheduleNotFoundError,
	RestaurantSchedulesInternalError,
	RestaurantsInternalError,
)
from src.restaurants.schemas import (
	CreateRestaurantScheduleSchema,
	CreateRestaurantSchema,
	UpdateRestaurantScheduleSchema,
	UpdateRestaurantSchema,
)


@pytest.mark.asyncio
async def test_list_restaurants_success(
	restaurant_service, mock_restaurant_repository, sample_restaurant
):
	mock_restaurant_repository.list = AsyncMock(return_value=[sample_restaurant])

	result = await restaurant_service.list(name='Pizza', owner_id=sample_restaurant.owner_id)

	assert len(result) == 1
	assert result[0].id == sample_restaurant.id

	mock_restaurant_repository.list.assert_awaited_once_with('Pizza', sample_restaurant.owner_id)


@pytest.mark.asyncio
async def test_list_restaurants_internal_error(restaurant_service, mock_restaurant_repository):
	mock_restaurant_repository.list = AsyncMock(side_effect=Exception('Ih! Deu ruim!'))

	with pytest.raises(RestaurantsInternalError) as exc_info:
		await restaurant_service.list(name='Pizza', owner_id=uuid4())

	assert 'Ih! Deu ruim!' in str(exc_info.value)

	mock_restaurant_repository.list.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_restaurant_success(
	restaurant_service, mock_restaurant_repository, sample_restaurant
):
	mock_restaurant_repository.get = AsyncMock(return_value=sample_restaurant)

	result = await restaurant_service.get(id=sample_restaurant.id)

	assert result.id == sample_restaurant.id
	assert result.name == sample_restaurant.name

	mock_restaurant_repository.get.assert_awaited_once_with(sample_restaurant.id)


@pytest.mark.asyncio
async def test_get_restaurant_not_found(restaurant_service, mock_restaurant_repository):
	restaurant_id = uuid4()
	mock_restaurant_repository.get = AsyncMock(
		side_effect=RestaurantNotFoundError(restaurant_id=str(restaurant_id))
	)

	with pytest.raises(RestaurantNotFoundError):
		await restaurant_service.get(id=restaurant_id)

	mock_restaurant_repository.get.assert_awaited_once_with(restaurant_id)


@pytest.mark.asyncio
async def test_get_restaurant_internal_error(restaurant_service, mock_restaurant_repository):
	restaurant_id = uuid4()
	mock_restaurant_repository.get = AsyncMock(side_effect=Exception('Ih! Deu ruim!'))

	with pytest.raises(RestaurantsInternalError) as exc_info:
		await restaurant_service.get(id=restaurant_id)

	assert 'Ih! Deu ruim!' in str(exc_info.value)

	mock_restaurant_repository.get.assert_awaited_once_with(restaurant_id)


@pytest.mark.asyncio
async def test_create_restaurant_success(restaurant_service, mock_restaurant_repository):
	restaurant_id = uuid4()
	create_data = CreateRestaurantSchema(
		name='New Restaurant',
		image_url=None,
		owner_id=uuid4(),
		street='Main St',
		number=100,
		neighborhood='Centro',
		city='São Paulo',
		state_abbr='SP',
	)
	mock_restaurant_repository.create = AsyncMock(return_value=restaurant_id)

	result = await restaurant_service.create(restaurant=create_data)

	assert result.id == restaurant_id

	mock_restaurant_repository.create.assert_awaited_once_with(create_data)


@pytest.mark.asyncio
async def test_create_restaurant_internal_error(restaurant_service, mock_restaurant_repository):
	create_data = CreateRestaurantSchema(
		name='New Restaurant',
		image_url=None,
		owner_id=uuid4(),
		street='Main St',
		number=100,
		neighborhood='Centro',
		city='São Paulo',
		state_abbr='SP',
	)
	mock_restaurant_repository.create = AsyncMock(side_effect=Exception('Ih! Deu ruim!'))

	with pytest.raises(RestaurantsInternalError) as exc_info:
		await restaurant_service.create(restaurant=create_data)

	assert 'Ih! Deu ruim!' in str(exc_info.value)

	mock_restaurant_repository.create.assert_awaited_once_with(create_data)


@pytest.mark.asyncio
async def test_update_restaurant_success(
	restaurant_service, mock_restaurant_repository, sample_restaurant
):
	update_data = UpdateRestaurantSchema(
		name='Updated Name',
		image_url=None,
		owner_id=sample_restaurant.owner_id,
		street='New Street',
		number=456,
		neighborhood='New Neighborhood',
		city='Rio de Janeiro',
		state_abbr='RJ',
	)
	mock_restaurant_repository.get = AsyncMock(return_value=sample_restaurant)
	mock_restaurant_repository.update = AsyncMock()

	result = await restaurant_service.update(id=sample_restaurant.id, restaurant_update=update_data)

	assert result.name == 'Updated Name'
	assert result.city == 'Rio de Janeiro'
	assert result.state_abbr == 'RJ'

	mock_restaurant_repository.get.assert_awaited_once_with(sample_restaurant.id)
	mock_restaurant_repository.update.assert_awaited_once_with(sample_restaurant)


@pytest.mark.asyncio
async def test_update_restaurant_not_found(restaurant_service, mock_restaurant_repository):
	restaurant_id = uuid4()
	update_data = UpdateRestaurantSchema(
		name='Updated Name',
		image_url=None,
		owner_id=uuid4(),
		street='Street',
		number=100,
		neighborhood='Neighborhood',
		city='City',
		state_abbr='SP',
	)
	mock_restaurant_repository.get = AsyncMock(
		side_effect=RestaurantNotFoundError(restaurant_id=str(restaurant_id))
	)

	with pytest.raises(RestaurantNotFoundError):
		await restaurant_service.update(id=restaurant_id, restaurant_update=update_data)

	mock_restaurant_repository.get.assert_awaited_once_with(restaurant_id)


@pytest.mark.asyncio
async def test_update_restaurant_internal_error(
	restaurant_service, mock_restaurant_repository, sample_restaurant
):
	update_data = UpdateRestaurantSchema(
		name='Updated Name',
		image_url=None,
		owner_id=sample_restaurant.owner_id,
		street='Street',
		number=100,
		neighborhood='Neighborhood',
		city='City',
		state_abbr='SP',
	)
	mock_restaurant_repository.get = AsyncMock(return_value=sample_restaurant)
	mock_restaurant_repository.update = AsyncMock(side_effect=Exception('Ih! Deu ruim!'))

	with pytest.raises(RestaurantsInternalError) as exc_info:
		await restaurant_service.update(id=sample_restaurant.id, restaurant_update=update_data)

	assert 'Ih! Deu ruim!' in str(exc_info.value)


@pytest.mark.asyncio
async def test_delete_restaurant_success(
	restaurant_service, mock_restaurant_repository, sample_restaurant
):
	mock_restaurant_repository.get = AsyncMock(return_value=sample_restaurant)
	mock_restaurant_repository.delete = AsyncMock()

	await restaurant_service.delete(id=sample_restaurant.id)

	mock_restaurant_repository.get.assert_awaited_once_with(sample_restaurant.id)
	mock_restaurant_repository.delete.assert_awaited_once_with(sample_restaurant)


@pytest.mark.asyncio
async def test_delete_restaurant_not_found(restaurant_service, mock_restaurant_repository):
	restaurant_id = uuid4()
	mock_restaurant_repository.get = AsyncMock(
		side_effect=RestaurantNotFoundError(restaurant_id=str(restaurant_id))
	)

	with pytest.raises(RestaurantNotFoundError):
		await restaurant_service.delete(id=restaurant_id)

	mock_restaurant_repository.get.assert_awaited_once_with(restaurant_id)


@pytest.mark.asyncio
async def test_delete_restaurant_internal_error(
	restaurant_service, mock_restaurant_repository, sample_restaurant
):
	mock_restaurant_repository.get = AsyncMock(return_value=sample_restaurant)
	mock_restaurant_repository.delete = AsyncMock(side_effect=Exception('Ih! Deu ruim!'))

	with pytest.raises(RestaurantsInternalError) as exc_info:
		await restaurant_service.delete(id=sample_restaurant.id)

	assert 'Ih! Deu ruim!' in str(exc_info.value)


@pytest.mark.asyncio
async def test_create_schedule_success(
	schedule_service, mock_schedule_repository, mock_restaurant_repository, sample_restaurant
):
	schedule_id = uuid4()
	create_data = CreateRestaurantScheduleSchema(
		day_type=DayType.WEEKDAY,
		start_day=Day.MONDAY,
		end_day=Day.FRIDAY,
		start_time='08:00:00',
		end_time='18:00:00',
	)
	mock_restaurant_repository.get = AsyncMock(return_value=sample_restaurant)
	mock_schedule_repository.get_by_restaurant = AsyncMock(return_value=[])
	mock_schedule_repository.create = AsyncMock(return_value=schedule_id)

	result = await schedule_service.create(restaurant_id=sample_restaurant.id, schedule=create_data)

	assert result.id == schedule_id

	mock_restaurant_repository.get.assert_awaited_once_with(sample_restaurant.id)
	mock_schedule_repository.get_by_restaurant.assert_awaited_once_with(sample_restaurant.id)
	mock_schedule_repository.create.assert_awaited_once_with(create_data, sample_restaurant.id)


@pytest.mark.asyncio
async def test_create_schedule_restaurant_not_found(schedule_service, mock_restaurant_repository):
	restaurant_id = uuid4()
	create_data = CreateRestaurantScheduleSchema(
		day_type=DayType.WEEKDAY,
		start_day=Day.MONDAY,
		end_day=Day.FRIDAY,
		start_time='08:00:00',
		end_time='18:00:00',
	)
	mock_restaurant_repository.get = AsyncMock(
		side_effect=RestaurantNotFoundError(restaurant_id=str(restaurant_id))
	)

	with pytest.raises(RestaurantNotFoundError):
		await schedule_service.create(restaurant_id=restaurant_id, schedule=create_data)

	mock_restaurant_repository.get.assert_awaited_once_with(restaurant_id)


@pytest.mark.asyncio
async def test_create_schedule_exceeds_limit(
	schedule_service,
	mock_schedule_repository,
	mock_restaurant_repository,
	sample_restaurant,
	sample_schedule,
):
	create_data = CreateRestaurantScheduleSchema(
		day_type=DayType.WEEKDAY,
		start_day=Day.MONDAY,
		end_day=Day.FRIDAY,
		start_time='08:00:00',
		end_time='18:00:00',
	)
	mock_restaurant_repository.get = AsyncMock(return_value=sample_restaurant)
	mock_schedule_repository.get_by_restaurant = AsyncMock(
		return_value=[sample_schedule, sample_schedule, sample_schedule]
	)

	with pytest.raises(RestaurantSchedulesInternalError) as exc_info:
		await schedule_service.create(restaurant_id=sample_restaurant.id, schedule=create_data)

	assert 'Cannot create more than three active schedules' in str(exc_info.value)

	mock_restaurant_repository.get.assert_awaited_once_with(sample_restaurant.id)
	mock_schedule_repository.get_by_restaurant.assert_awaited_once_with(sample_restaurant.id)


@pytest.mark.asyncio
async def test_create_schedule_internal_error(
	schedule_service, mock_schedule_repository, mock_restaurant_repository, sample_restaurant
):
	create_data = CreateRestaurantScheduleSchema(
		day_type=DayType.WEEKDAY,
		start_day=Day.MONDAY,
		end_day=Day.FRIDAY,
		start_time='08:00:00',
		end_time='18:00:00',
	)
	mock_restaurant_repository.get = AsyncMock(return_value=sample_restaurant)
	mock_schedule_repository.get_by_restaurant = AsyncMock(return_value=[])
	mock_schedule_repository.create = AsyncMock(side_effect=Exception('Ih! Deu ruim!'))

	with pytest.raises(RestaurantSchedulesInternalError) as exc_info:
		await schedule_service.create(restaurant_id=sample_restaurant.id, schedule=create_data)

	assert 'Ih! Deu ruim!' in str(exc_info.value)


@pytest.mark.asyncio
async def test_update_schedule_success(
	schedule_service,
	mock_schedule_repository,
	mock_restaurant_repository,
	sample_restaurant,
	sample_schedule,
):
	update_data = UpdateRestaurantScheduleSchema(
		day_type=DayType.WEEKEND,
		start_day=Day.SATURDAY,
		end_day=Day.SUNDAY,
		start_time='10:00:00',
		end_time='22:00:00',
	)
	mock_restaurant_repository.get = AsyncMock(return_value=sample_restaurant)
	mock_schedule_repository.get = AsyncMock(return_value=sample_schedule)
	mock_schedule_repository.update = AsyncMock()

	result = await schedule_service.update(
		restaurant_id=sample_restaurant.id,
		schedule_id=sample_schedule.id,
		schedule_update=update_data,
	)

	assert result.day_type == 'weekend'
	assert result.start_day == 'saturday'
	assert result.end_day == 'sunday'

	mock_restaurant_repository.get.assert_awaited_once_with(sample_restaurant.id)
	mock_schedule_repository.get.assert_awaited_once_with(sample_schedule.id)
	mock_schedule_repository.update.assert_awaited_once_with(sample_schedule)


@pytest.mark.asyncio
async def test_update_schedule_restaurant_not_found(schedule_service, mock_restaurant_repository):
	restaurant_id = uuid4()
	schedule_id = uuid4()
	update_data = UpdateRestaurantScheduleSchema(
		day_type=DayType.WEEKEND,
		start_day=Day.SATURDAY,
		end_day=Day.SUNDAY,
		start_time='10:00:00',
		end_time='22:00:00',
	)
	mock_restaurant_repository.get = AsyncMock(
		side_effect=RestaurantNotFoundError(restaurant_id=str(restaurant_id))
	)

	with pytest.raises(RestaurantNotFoundError):
		await schedule_service.update(
			restaurant_id=restaurant_id, schedule_id=schedule_id, schedule_update=update_data
		)

	mock_restaurant_repository.get.assert_awaited_once_with(restaurant_id)


@pytest.mark.asyncio
async def test_update_schedule_not_found(
	schedule_service, mock_schedule_repository, mock_restaurant_repository, sample_restaurant
):
	schedule_id = uuid4()
	update_data = UpdateRestaurantScheduleSchema(
		day_type=DayType.WEEKEND,
		start_day=Day.SATURDAY,
		end_day=Day.SUNDAY,
		start_time='10:00:00',
		end_time='22:00:00',
	)
	mock_restaurant_repository.get = AsyncMock(return_value=sample_restaurant)
	mock_schedule_repository.get = AsyncMock(
		side_effect=RestaurantScheduleNotFoundError(schedule_id=str(schedule_id))
	)

	with pytest.raises(RestaurantScheduleNotFoundError):
		await schedule_service.update(
			restaurant_id=sample_restaurant.id, schedule_id=schedule_id, schedule_update=update_data
		)

	mock_restaurant_repository.get.assert_awaited_once_with(sample_restaurant.id)
	mock_schedule_repository.get.assert_awaited_once_with(schedule_id)


@pytest.mark.asyncio
async def test_update_schedule_internal_error(
	schedule_service,
	mock_schedule_repository,
	mock_restaurant_repository,
	sample_restaurant,
	sample_schedule,
):
	update_data = UpdateRestaurantScheduleSchema(
		day_type=DayType.WEEKEND,
		start_day=Day.SATURDAY,
		end_day=Day.SUNDAY,
		start_time='10:00:00',
		end_time='22:00:00',
	)
	mock_restaurant_repository.get = AsyncMock(return_value=sample_restaurant)
	mock_schedule_repository.get = AsyncMock(return_value=sample_schedule)
	mock_schedule_repository.update = AsyncMock(side_effect=Exception('Ih! Deu ruim!'))

	with pytest.raises(RestaurantSchedulesInternalError) as exc_info:
		await schedule_service.update(
			restaurant_id=sample_restaurant.id,
			schedule_id=sample_schedule.id,
			schedule_update=update_data,
		)

	assert 'Ih! Deu ruim!' in str(exc_info.value)


@pytest.mark.asyncio
async def test_delete_schedule_success(
	schedule_service,
	mock_schedule_repository,
	mock_restaurant_repository,
	sample_restaurant,
	sample_schedule,
):
	mock_restaurant_repository.get = AsyncMock(return_value=sample_restaurant)
	mock_schedule_repository.get = AsyncMock(return_value=sample_schedule)
	mock_schedule_repository.delete = AsyncMock()

	await schedule_service.delete(
		restaurant_id=sample_restaurant.id, schedule_id=sample_schedule.id
	)

	mock_restaurant_repository.get.assert_awaited_once_with(sample_restaurant.id)
	mock_schedule_repository.get.assert_awaited_once_with(sample_schedule.id)
	mock_schedule_repository.delete.assert_awaited_once_with(sample_schedule)


@pytest.mark.asyncio
async def test_delete_schedule_restaurant_not_found(schedule_service, mock_restaurant_repository):
	restaurant_id = uuid4()
	schedule_id = uuid4()
	mock_restaurant_repository.get = AsyncMock(
		side_effect=RestaurantNotFoundError(restaurant_id=str(restaurant_id))
	)

	with pytest.raises(RestaurantNotFoundError):
		await schedule_service.delete(restaurant_id=restaurant_id, schedule_id=schedule_id)

	mock_restaurant_repository.get.assert_awaited_once_with(restaurant_id)


@pytest.mark.asyncio
async def test_delete_schedule_not_found(
	schedule_service, mock_schedule_repository, mock_restaurant_repository, sample_restaurant
):
	schedule_id = uuid4()
	mock_restaurant_repository.get = AsyncMock(return_value=sample_restaurant)
	mock_schedule_repository.get = AsyncMock(
		side_effect=RestaurantScheduleNotFoundError(schedule_id=str(schedule_id))
	)

	with pytest.raises(RestaurantScheduleNotFoundError):
		await schedule_service.delete(restaurant_id=sample_restaurant.id, schedule_id=schedule_id)

	mock_restaurant_repository.get.assert_awaited_once_with(sample_restaurant.id)
	mock_schedule_repository.get.assert_awaited_once_with(schedule_id)


@pytest.mark.asyncio
async def test_delete_schedule_internal_error(
	schedule_service,
	mock_schedule_repository,
	mock_restaurant_repository,
	sample_restaurant,
	sample_schedule,
):
	mock_restaurant_repository.get = AsyncMock(return_value=sample_restaurant)
	mock_schedule_repository.get = AsyncMock(return_value=sample_schedule)
	mock_schedule_repository.delete = AsyncMock(side_effect=Exception('Ih! Deu ruim!'))

	with pytest.raises(RestaurantSchedulesInternalError) as exc_info:
		await schedule_service.delete(
			restaurant_id=sample_restaurant.id, schedule_id=sample_schedule.id
		)

	assert 'Ih! Deu ruim!' in str(exc_info.value)
