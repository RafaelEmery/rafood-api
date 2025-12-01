from uuid import uuid4

import pytest

from src.categories.models import Category
from src.restaurants.models import Restaurant
from src.users.models import User


@pytest.fixture
def user_factory():
	def create(session, **kwargs):
		obj = User(
			id=uuid4(),
			first_name=kwargs.get('first_name', 'John'),
			last_name=kwargs.get('last_name', 'Doe'),
			email=kwargs.get('email', f'user_{uuid4()}@example.com'),
			password=kwargs.get('password', 'password123'),
		)
		session.add(obj)
		return obj

	return create


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
def category_factory():
	def create(session, **kwargs):
		obj = Category(id=uuid4(), name=kwargs.get('name', 'By Factory'))
		session.add(obj)

		return obj

	return create
