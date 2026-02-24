from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.users.exceptions import UserNotFoundError, UsersInternalError
from src.users.schemas import (
	CreateUserSchema,
	UpdateUserSchema,
)


@pytest.mark.asyncio
async def test_list_users_success(user_service, mock_user_repository, sample_user_schema):
	mock_user_repository.list = AsyncMock(return_value=[sample_user_schema])

	result = await user_service.list()

	assert len(result) == 1
	assert result[0].id == sample_user_schema.id

	mock_user_repository.list.assert_awaited_once()


@pytest.mark.asyncio
async def test_list_users_internal_error(user_service, mock_user_repository):
	mock_user_repository.list = AsyncMock(side_effect=Exception('Ih! Deu ruim!'))

	with pytest.raises(UsersInternalError) as exc_info:
		await user_service.list()

	assert 'Ih! Deu ruim!' in str(exc_info.value)

	mock_user_repository.list.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_user_success(user_service, mock_user_repository, sample_user_details_schema):
	mock_user_repository.get = AsyncMock(return_value=sample_user_details_schema)

	result = await user_service.get(id=sample_user_details_schema.id)

	assert result.id == sample_user_details_schema.id
	assert result.first_name == sample_user_details_schema.first_name

	mock_user_repository.get.assert_awaited_once_with(sample_user_details_schema.id)


@pytest.mark.asyncio
async def test_get_user_not_found(user_service, mock_user_repository):
	user_id = uuid4()
	mock_user_repository.get = AsyncMock(side_effect=UserNotFoundError(user_id=str(user_id)))

	with pytest.raises(UserNotFoundError):
		await user_service.get(id=user_id)

	mock_user_repository.get.assert_awaited_once_with(user_id)


@pytest.mark.asyncio
async def test_get_user_internal_error(user_service, mock_user_repository):
	user_id = uuid4()
	mock_user_repository.get = AsyncMock(side_effect=Exception('Ih! Deu ruim!'))

	with pytest.raises(UsersInternalError) as exc_info:
		await user_service.get(id=user_id)

	assert 'Ih! Deu ruim!' in str(exc_info.value)

	mock_user_repository.get.assert_awaited_once_with(user_id)


@pytest.mark.asyncio
async def test_create_user_success(user_service, mock_user_repository):
	user_id = uuid4()
	create_data = CreateUserSchema(
		first_name='Rafael',
		last_name='Cade',
		password='password123',
		email='rafael@example.com',
	)
	mock_user_repository.create = AsyncMock(return_value=user_id)

	result = await user_service.create(user=create_data)

	assert result.id == user_id

	mock_user_repository.create.assert_awaited_once_with(create_data)


@pytest.mark.asyncio
async def test_create_user_internal_error(user_service, mock_user_repository):
	create_data = CreateUserSchema(
		first_name='Rafael',
		last_name='Cade',
		password='password123',
		email='rafael@example.com',
	)
	mock_user_repository.create = AsyncMock(side_effect=Exception('Ih! Deu ruim!'))

	with pytest.raises(UsersInternalError) as exc_info:
		await user_service.create(user=create_data)

	assert 'Ih! Deu ruim!' in str(exc_info.value)

	mock_user_repository.create.assert_awaited_once_with(create_data)


@pytest.mark.asyncio
async def test_update_user_success(user_service, mock_user_repository, sample_user_schema):
	update_data = UpdateUserSchema(
		first_name='Rafa',
		last_name='Cade',
	)
	mock_user_repository.get = AsyncMock(return_value=sample_user_schema)
	mock_user_repository.update = AsyncMock()

	result = await user_service.update(id=sample_user_schema.id, user_update=update_data)

	assert result.first_name == 'Rafa'
	assert result.last_name == 'Cade'

	mock_user_repository.get.assert_awaited_once_with(sample_user_schema.id)
	mock_user_repository.update.assert_awaited_once_with(sample_user_schema)


@pytest.mark.asyncio
async def test_update_user_not_found(user_service, mock_user_repository):
	user_id = uuid4()
	update_data = UpdateUserSchema(
		first_name='Rafa',
		last_name='Cade',
	)
	mock_user_repository.get = AsyncMock(side_effect=UserNotFoundError(user_id=str(user_id)))

	with pytest.raises(UserNotFoundError):
		await user_service.update(id=user_id, user_update=update_data)

	mock_user_repository.get.assert_awaited_once_with(user_id)


@pytest.mark.asyncio
async def test_update_user_internal_error(user_service, mock_user_repository, sample_user_schema):
	update_data = UpdateUserSchema(
		first_name='Rafa',
		last_name='Cade',
	)
	mock_user_repository.get = AsyncMock(return_value=sample_user_schema)
	mock_user_repository.update = AsyncMock(side_effect=Exception('Ih! Deu ruim!'))

	with pytest.raises(UsersInternalError) as exc_info:
		await user_service.update(id=sample_user_schema.id, user_update=update_data)

	assert 'Ih! Deu ruim!' in str(exc_info.value)


@pytest.mark.asyncio
async def test_delete_user_success(user_service, mock_user_repository, sample_user_schema):
	mock_user_repository.get = AsyncMock(return_value=sample_user_schema)
	mock_user_repository.delete = AsyncMock()

	await user_service.delete(id=sample_user_schema.id)

	mock_user_repository.get.assert_awaited_once_with(sample_user_schema.id)
	mock_user_repository.delete.assert_awaited_once_with(sample_user_schema)


@pytest.mark.asyncio
async def test_delete_user_not_found(user_service, mock_user_repository):
	user_id = uuid4()
	mock_user_repository.get = AsyncMock(side_effect=UserNotFoundError(user_id=str(user_id)))

	with pytest.raises(UserNotFoundError):
		await user_service.delete(id=user_id)

	mock_user_repository.get.assert_awaited_once_with(user_id)


@pytest.mark.asyncio
async def test_delete_user_internal_error(user_service, mock_user_repository, sample_user_schema):
	mock_user_repository.get = AsyncMock(return_value=sample_user_schema)
	mock_user_repository.delete = AsyncMock(side_effect=Exception('Ih! Deu ruim!'))

	with pytest.raises(UsersInternalError) as exc_info:
		await user_service.delete(id=sample_user_schema.id)

	assert 'Ih! Deu ruim!' in str(exc_info.value)
