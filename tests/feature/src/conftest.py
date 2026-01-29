from uuid import uuid4

import pytest

from src.categories.models import Category
from src.offers.models import Offer
from src.products.models import Product
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
		obj = Category(id=uuid4(), name=kwargs.get('name', f'By Factory {str(uuid4())}'))
		session.add(obj)

		return obj

	return create


@pytest.fixture
def offer_factory(product_factory):
	def create(session, **kwargs):
		# Create product if not provided
		if 'product_id' not in kwargs:
			product = product_factory(session)
			kwargs['product_id'] = product.id

		obj = Offer(
			id=uuid4(),
			product_id=kwargs['product_id'],
			price=kwargs.get('price', 19.99),
			active=kwargs.get('active', True),
		)
		session.add(obj)

		return obj

	return create


@pytest.fixture
def product_factory(restaurant_factory, category_factory):
	def create(session, **kwargs):
		# Create restaurant if not provided
		if 'restaurant_id' not in kwargs:
			restaurant = restaurant_factory(session)
			kwargs['restaurant_id'] = restaurant.id

		# Create category if not provided
		if 'category_id' not in kwargs:
			category = category_factory(session)
			kwargs['category_id'] = category.id

		obj = Product(
			id=uuid4(),
			restaurant_id=kwargs['restaurant_id'],
			name=kwargs.get('name', 'Product By Factory'),
			price=kwargs.get('price', 29.99),
			category_id=kwargs['category_id'],
			image_url=kwargs.get('image_url', 'https://example.com/product.jpg'),
		)
		session.add(obj)

		return obj

	return create
