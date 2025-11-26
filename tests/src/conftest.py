from uuid import uuid4

import pytest

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
