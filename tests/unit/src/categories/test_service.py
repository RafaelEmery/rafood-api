from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.categories.exceptions import CategoriesInternalError, CategoryNotFoundError
from src.categories.schemas import (
	CreateCategorySchema,
)


@pytest.mark.asyncio
async def test_list_categories_success(
	category_service, mock_category_repository, sample_category_schema
):
	mock_category_repository.list = AsyncMock(return_value=[sample_category_schema])

	result = await category_service.list()

	assert len(result) == 1
	assert result[0].id == sample_category_schema.id

	mock_category_repository.list.assert_awaited_once()


@pytest.mark.asyncio
async def test_list_categories_internal_error(category_service, mock_category_repository):
	mock_category_repository.list = AsyncMock(side_effect=Exception('Ih! Deu ruim!'))

	with pytest.raises(CategoriesInternalError) as exc_info:
		await category_service.list()

	assert 'Ih! Deu ruim!' in str(exc_info.value)

	mock_category_repository.list.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_category_success(category_service, mock_category_repository):
	category_id = uuid4()
	create_data = CreateCategorySchema(
		name='Pizza',
	)
	mock_category_repository.create = AsyncMock(return_value=category_id)

	result = await category_service.create(category=create_data)

	assert result.id == category_id

	mock_category_repository.create.assert_awaited_once_with(create_data)


@pytest.mark.asyncio
async def test_create_category_internal_error(category_service, mock_category_repository):
	create_data = CreateCategorySchema(
		name='Pizza',
	)
	mock_category_repository.create = AsyncMock(side_effect=Exception('Ih! Deu ruim!'))

	with pytest.raises(CategoriesInternalError) as exc_info:
		await category_service.create(category=create_data)

	assert 'Ih! Deu ruim!' in str(exc_info.value)

	mock_category_repository.create.assert_awaited_once_with(create_data)


@pytest.mark.asyncio
async def test_delete_category_success(
	category_service, mock_category_repository, sample_category_schema
):
	mock_category_repository.get = AsyncMock(return_value=sample_category_schema)
	mock_category_repository.delete = AsyncMock()

	await category_service.delete(id=sample_category_schema.id)

	mock_category_repository.get.assert_awaited_once_with(sample_category_schema.id)
	mock_category_repository.delete.assert_awaited_once_with(sample_category_schema)


@pytest.mark.asyncio
async def test_delete_category_not_found(category_service, mock_category_repository):
	category_id = uuid4()
	mock_category_repository.get = AsyncMock(
		side_effect=CategoryNotFoundError(category_id=str(category_id))
	)

	with pytest.raises(CategoryNotFoundError):
		await category_service.delete(id=category_id)

	mock_category_repository.get.assert_awaited_once_with(category_id)


@pytest.mark.asyncio
async def test_delete_category_internal_error(
	category_service, mock_category_repository, sample_category_schema
):
	mock_category_repository.get = AsyncMock(return_value=sample_category_schema)
	mock_category_repository.delete = AsyncMock(side_effect=Exception('Ih! Deu ruim!'))

	with pytest.raises(CategoriesInternalError) as exc_info:
		await category_service.delete(id=sample_category_schema.id)

	assert 'Ih! Deu ruim!' in str(exc_info.value)
