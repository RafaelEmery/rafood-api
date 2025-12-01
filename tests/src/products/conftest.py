from uuid import uuid4

import pytest

from src.products.models import Product


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


@pytest.fixture
def build_create_payload():
	def _build(restaurant_id=None, category_id=None):
		return {
			'restaurant_id': str(restaurant_id) if restaurant_id else str(uuid4()),
			'name': 'Léo Pereira',
			'price': 29.99,
			'category_id': str(category_id) if category_id else str(uuid4()),
			'image_url': 'https://example.com/product.jpg',
		}

	return _build


@pytest.fixture
def build_update_payload():
	def _build(restaurant_id=None, category_id=None):
		return {
			'restaurant_id': str(restaurant_id) if restaurant_id else str(uuid4()),
			'name': 'Alex Sandro',
			'price': 39.99,
			'category_id': str(category_id) if category_id else str(uuid4()),
			'image_url': 'https://new-example.com/updated.jpg',
		}

	return _build
