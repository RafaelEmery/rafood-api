from uuid import uuid4

import pytest

from src.categories.models import Category
from src.users.models import User


@pytest.fixture
def category():
	return Category(id=uuid4(), name='Danilo')


@pytest.fixture
def user():
	return User(
		id=uuid4(),
		first_name='Léo',
		last_name='Ortiz',
		email='leo@ortiz.com',
		password=str(uuid4()),
	)
