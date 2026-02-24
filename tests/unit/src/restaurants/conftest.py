from datetime import datetime, time
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from src.restaurants.models import Restaurant, RestaurantSchedule
from src.restaurants.repository import RestaurantRepository, RestaurantScheduleRepository
from src.restaurants.service import RestaurantScheduleService, RestaurantService


@pytest.fixture
def mock_restaurant_repository():
	return MagicMock(spec=RestaurantRepository)


@pytest.fixture
def mock_schedule_repository():
	return MagicMock(spec=RestaurantScheduleRepository)


@pytest.fixture
def restaurant_service(mock_restaurant_repository):
	return RestaurantService(repository=mock_restaurant_repository)


@pytest.fixture
def schedule_service(mock_schedule_repository, mock_restaurant_repository):
	return RestaurantScheduleService(
		repository=mock_schedule_repository, restaurant_repository=mock_restaurant_repository
	)


@pytest.fixture
def sample_restaurant():
	restaurant_id = uuid4()
	owner_id = uuid4()
	return Restaurant(
		id=restaurant_id,
		name='Pizza Palace',
		image_url='https://example.com/image.jpg',
		owner_id=owner_id,
		street='Main Street',
		number=123,
		neighborhood='Downtown',
		city='São Paulo',
		state_abbr='SP',
		created_at=datetime.now(),
		updated_at=datetime.now(),
	)


@pytest.fixture
def sample_schedule():
	return RestaurantSchedule(
		id=uuid4(),
		restaurant_id=uuid4(),
		day_type='weekday',
		start_day='monday',
		end_day='friday',
		start_time=time(8, 0, 0),
		end_time=time(18, 0, 0),
		created_at=datetime.now(),
		updated_at=datetime.now(),
	)
