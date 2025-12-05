from uuid import uuid4

import pytest


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
