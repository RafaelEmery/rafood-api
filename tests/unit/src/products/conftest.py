from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from src.core.db.unit_of_work import UnitOfWork
from src.core.outbox.service import OutboxService
from src.products.models import Product
from src.products.repository import ProductRepository
from src.products.schemas import ProductWithCategoriesSchema, ProductWithOffersSchema
from src.products.service import ProductService


@pytest.fixture
def mock_product_repository():
	return MagicMock(spec=ProductRepository)


@pytest.fixture
def mock_outbox_service():
	return MagicMock(spec=OutboxService)


@pytest.fixture
def mock_unit_of_work():
	uow = MagicMock(spec=UnitOfWork)
	uow.commit = AsyncMock()
	uow.rollback = AsyncMock()
	return uow


@pytest.fixture
def product_service(mock_product_repository, mock_outbox_service, mock_unit_of_work):
	return ProductService(
		repository=mock_product_repository,
		outbox_service=mock_outbox_service,
		uow=mock_unit_of_work,
	)


@pytest.fixture
def sample_product():
	product_id = uuid4()
	restaurant_id = uuid4()
	category_id = uuid4()
	return Product(
		id=product_id,
		restaurant_id=restaurant_id,
		name='Pizza Margherita',
		price=25.0,
		category_id=category_id,
		image_url='https://example.com/pizza.jpg',
		created_at=datetime.now(),
		updated_at=datetime.now(),
	)


@pytest.fixture
def sample_product_with_categories(sample_product):
	return ProductWithCategoriesSchema(
		id=sample_product.id,
		restaurant_id=sample_product.restaurant_id,
		name=sample_product.name,
		price=sample_product.price,
		category_id=sample_product.category_id,
		image_url=sample_product.image_url,
		categories=[],
		category={
			'id': uuid4(),
			'name': 'Test Category',
			'created_at': datetime.now(),
			'updated_at': datetime.now(),
		},
		created_at=sample_product.created_at,
		updated_at=sample_product.updated_at,
	)


@pytest.fixture
def sample_product_with_offers(sample_product):
	return ProductWithOffersSchema(
		id=sample_product.id,
		restaurant_id=sample_product.restaurant_id,
		name=sample_product.name,
		price=sample_product.price,
		category_id=sample_product.category_id,
		image_url=sample_product.image_url,
		offers=[],
		created_at=sample_product.created_at,
		updated_at=sample_product.updated_at,
	)
