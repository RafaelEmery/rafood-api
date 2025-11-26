from uuid import uuid4

import pytest

from src.categories.models import Category


@pytest.fixture
def category_factory():
	def create(session, **kwargs):
		obj = Category(id=uuid4(), name=kwargs.get('name', 'By Factory'))
		session.add(obj)

		return obj

	return create
