from datetime import datetime
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from src.users.models import User
from src.users.repository import UserRepository
from src.users.schemas import (
	UserDetailsSchema,
	UserSchema,
)
from src.users.service import UserService


@pytest.fixture
def mock_user_repository():
	return MagicMock(spec=UserRepository)


@pytest.fixture
def user_service(mock_user_repository):
	return UserService(repository=mock_user_repository)


@pytest.fixture
def sample_user():
	user_id = uuid4()
	return User(
		id=user_id,
		first_name='Rafael',
		last_name='Cade',
		email='rafael@example.com',
		created_at=datetime.now(),
		updated_at=datetime.now(),
	)


@pytest.fixture
def sample_user_schema(sample_user):
	return UserSchema(
		id=sample_user.id,
		first_name=sample_user.first_name,
		last_name=sample_user.last_name,
		email=sample_user.email,
		created_at=sample_user.created_at,
		updated_at=sample_user.updated_at,
	)


@pytest.fixture
def sample_user_details_schema(sample_user):
	return UserDetailsSchema(
		id=sample_user.id,
		first_name=sample_user.first_name,
		last_name=sample_user.last_name,
		email=sample_user.email,
		created_at=sample_user.created_at,
		updated_at=sample_user.updated_at,
	)
