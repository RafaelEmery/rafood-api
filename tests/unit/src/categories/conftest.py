from datetime import datetime
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from src.categories.models import Category
from src.categories.repository import CategoryRepository
from src.categories.schemas import (
	CategorySchema,
)
from src.categories.service import CategoryService


@pytest.fixture
def mock_category_repository():
	return MagicMock(spec=CategoryRepository)


@pytest.fixture
def category_service(mock_category_repository):
	return CategoryService(repository=mock_category_repository)


@pytest.fixture
def sample_category():
	category_id = uuid4()
	return Category(
		id=category_id,
		name='Pizza',
		created_at=datetime.now(),
		updated_at=datetime.now(),
	)


@pytest.fixture
def sample_category_schema(sample_category):
	return CategorySchema(
		id=sample_category.id,
		name=sample_category.name,
		created_at=sample_category.created_at,
		updated_at=sample_category.updated_at,
	)
