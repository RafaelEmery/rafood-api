from datetime import time
from uuid import uuid4

import pytest

from src.restaurants.models import Restaurant, RestaurantSchedule


@pytest.fixture
def restaurant_factory(user_factory):
	def create(session, **kwargs):
		# Create owner if not provided
		if 'owner_id' not in kwargs:
			owner = user_factory(session)
			session.add(owner)
			kwargs['owner_id'] = owner.id

		obj = Restaurant(
			id=uuid4(),
			name=kwargs.get('name', 'Restaurant By Factory'),
			image_url=kwargs.get('image_url', 'https://example.com/image.jpg'),
			owner_id=kwargs['owner_id'],
			street=kwargs.get('street', 'Main Street'),
			number=kwargs.get('number', 123),
			neighborhood=kwargs.get('neighborhood', 'Downtown'),
			city=kwargs.get('city', 'São Paulo'),
			state_abbr=kwargs.get('state_abbr', 'SP'),
		)
		session.add(obj)

		return obj

	return create


@pytest.fixture
def restaurant_schedule_factory(user_factory, restaurant_factory):
	def create(session, **kwargs):
		# Create restaurant if not provided
		if 'restaurant_id' not in kwargs:
			owner = user_factory(session)
			restaurant = restaurant_factory(session, owner_id=owner.id)
			kwargs['restaurant_id'] = restaurant.id
			session.add(owner)

			restaurant = restaurant_factory(session, owner_id=owner.id)
			session.add(restaurant)
			kwargs['restaurant_id'] = restaurant.id

		obj = RestaurantSchedule(
			id=uuid4(),
			restaurant_id=kwargs['restaurant_id'],
			day_type=kwargs.get('day_type', 'weekday'),
			start_day=kwargs.get('start_day', 'monday'),
			end_day=kwargs.get('end_day', 'friday'),
			start_time=kwargs.get('start_time', time(9, 0)),
			end_time=kwargs.get('end_time', time(18, 0)),
		)
		session.add(obj)

		return obj

	return create


@pytest.fixture
def build_create_payload():
	def _build(owner_id=None):
		return {
			'name': 'Jorginho',
			'image_url': 'https://example.com/testaurant.jpg',
			'owner_id': str(owner_id) if owner_id else str(uuid4()),
			'street': 'Test Street',
			'number': 101,
			'neighborhood': 'Test Neighborhood',
			'city': 'Test City',
			'state_abbr': 'TS',
		}

	return _build


@pytest.fixture
def build_update_payload():
	def _build(owner_id=None):
		return {
			'name': 'Erick Pulgar',
			'image_url': 'https://example.com/new-image.jpg',
			'owner_id': str(owner_id) if owner_id else str(uuid4()),
			'street': 'Test Street',
			'number': 101,
			'neighborhood': 'Test Neighborhood',
			'city': 'Test City',
			'state_abbr': 'TS',
		}

	return _build


@pytest.fixture
def build_schedule_create_payload():
	def _build():
		return {
			'day_type': 'weekday',
			'start_day': 'monday',
			'end_day': 'friday',
			'start_time': '09:00:00',
			'end_time': '18:00:00',
		}

	return _build


@pytest.fixture
def build_schedule_update_payload():
	def _build():
		return {
			'day_type': 'weekday',
			'start_day': 'monday',
			'end_day': 'tuesday',
			'start_time': '18:00:00',
			'end_time': '23:00:00',
		}

	return _build
