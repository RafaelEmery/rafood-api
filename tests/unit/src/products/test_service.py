from unittest.mock import ANY, AsyncMock
from uuid import uuid4

import pytest

from src.products.exceptions import ProductNotFoundError, ProductsInternalError
from src.products.schemas import (
	CreateProductSchema,
	UpdateProductSchema,
)


@pytest.mark.asyncio
async def test_list_products_success(
	product_service, mock_product_repository, sample_product_with_categories
):
	mock_product_repository.list = AsyncMock(return_value=[sample_product_with_categories])

	result = await product_service.list(
		name='Pizza', category_id=sample_product_with_categories.category_id
	)

	assert len(result) == 1
	assert result[0].id == sample_product_with_categories.id

	mock_product_repository.list.assert_awaited_once_with(
		'Pizza', sample_product_with_categories.category_id
	)


@pytest.mark.asyncio
async def test_list_products_internal_error(product_service, mock_product_repository):
	mock_product_repository.list = AsyncMock(side_effect=Exception('Ih! Deu ruim!'))

	with pytest.raises(ProductsInternalError) as exc_info:
		await product_service.list(name='Pizza', category_id=uuid4())

	assert 'Ih! Deu ruim!' in str(exc_info.value)

	mock_product_repository.list.assert_awaited_once_with('Pizza', ANY)


@pytest.mark.asyncio
async def test_get_product_success(
	product_service, mock_product_repository, sample_product_with_offers
):
	mock_product_repository.get = AsyncMock(return_value=sample_product_with_offers)

	result = await product_service.get(id=sample_product_with_offers.id)

	assert result.id == sample_product_with_offers.id
	assert result.name == sample_product_with_offers.name

	mock_product_repository.get.assert_awaited_once_with(sample_product_with_offers.id)


@pytest.mark.asyncio
async def test_get_product_not_found(product_service, mock_product_repository):
	product_id = uuid4()
	mock_product_repository.get = AsyncMock(
		side_effect=ProductNotFoundError(product_id=str(product_id))
	)

	with pytest.raises(ProductNotFoundError):
		await product_service.get(id=product_id)

	mock_product_repository.get.assert_awaited_once_with(product_id)


@pytest.mark.asyncio
async def test_get_product_internal_error(product_service, mock_product_repository):
	product_id = uuid4()
	mock_product_repository.get = AsyncMock(side_effect=Exception('Ih! Deu ruim!'))

	with pytest.raises(ProductsInternalError) as exc_info:
		await product_service.get(id=product_id)

	assert 'Ih! Deu ruim!' in str(exc_info.value)

	mock_product_repository.get.assert_awaited_once_with(product_id)


@pytest.mark.asyncio
async def test_create_product_success(product_service, mock_product_repository):
	product_id = uuid4()
	create_data = CreateProductSchema(
		restaurant_id=uuid4(),
		name='Pizza Margherita',
		price=25.0,
		category_id=uuid4(),
		image_url='https://example.com/pizza.jpg',
	)
	mock_product_repository.create = AsyncMock(return_value=product_id)

	result = await product_service.create(product=create_data)

	assert result.id == product_id

	mock_product_repository.create.assert_awaited_once_with(create_data)


@pytest.mark.asyncio
async def test_create_product_internal_error(product_service, mock_product_repository):
	create_data = CreateProductSchema(
		restaurant_id=uuid4(),
		name='Pizza Margherita',
		price=25.0,
		category_id=uuid4(),
		image_url='https://example.com/pizza.jpg',
	)
	mock_product_repository.create = AsyncMock(side_effect=Exception('Ih! Deu ruim!'))

	with pytest.raises(ProductsInternalError) as exc_info:
		await product_service.create(product=create_data)

	assert 'Ih! Deu ruim!' in str(exc_info.value)

	mock_product_repository.create.assert_awaited_once_with(create_data)


@pytest.mark.asyncio
async def test_update_product_success(product_service, mock_product_repository, sample_product):
	update_data = UpdateProductSchema(
		restaurant_id=sample_product.restaurant_id,
		name='Pizza Pepperoni',
		price=30.0,
		category_id=sample_product.category_id,
		image_url='https://example.com/pepperoni.jpg',
	)
	mock_product_repository.get = AsyncMock(return_value=sample_product)
	mock_product_repository.update = AsyncMock()

	result = await product_service.update(id=sample_product.id, product_update=update_data)

	assert result.name == 'Pizza Pepperoni'
	assert result.price == 30.0
	assert result.image_url == 'https://example.com/pepperoni.jpg'

	mock_product_repository.get.assert_awaited_once_with(sample_product.id)
	mock_product_repository.update.assert_awaited_once_with(sample_product)


@pytest.mark.asyncio
async def test_update_product_not_found(product_service, mock_product_repository):
	product_id = uuid4()
	update_data = UpdateProductSchema(
		restaurant_id=uuid4(),
		name='Pizza Pepperoni',
		price=30.0,
		category_id=uuid4(),
		image_url='https://example.com/pepperoni.jpg',
	)
	mock_product_repository.get = AsyncMock(
		side_effect=ProductNotFoundError(product_id=str(product_id))
	)

	with pytest.raises(ProductNotFoundError):
		await product_service.update(id=product_id, product_update=update_data)

	mock_product_repository.get.assert_awaited_once_with(product_id)


@pytest.mark.asyncio
async def test_update_product_internal_error(
	product_service, mock_product_repository, sample_product
):
	update_data = UpdateProductSchema(
		restaurant_id=sample_product.restaurant_id,
		name='Pizza Pepperoni',
		price=30.0,
		category_id=sample_product.category_id,
		image_url='https://example.com/pepperoni.jpg',
	)
	mock_product_repository.get = AsyncMock(return_value=sample_product)
	mock_product_repository.update = AsyncMock(side_effect=Exception('Ih! Deu ruim!'))

	with pytest.raises(ProductsInternalError) as exc_info:
		await product_service.update(id=sample_product.id, product_update=update_data)

	assert 'Ih! Deu ruim!' in str(exc_info.value)


@pytest.mark.asyncio
async def test_delete_product_success(product_service, mock_product_repository, sample_product):
	mock_product_repository.get = AsyncMock(return_value=sample_product)
	mock_product_repository.delete = AsyncMock()

	await product_service.delete(id=sample_product.id)

	mock_product_repository.get.assert_awaited_once_with(sample_product.id)
	mock_product_repository.delete.assert_awaited_once_with(sample_product)


@pytest.mark.asyncio
async def test_delete_product_not_found(product_service, mock_product_repository):
	product_id = uuid4()
	mock_product_repository.get = AsyncMock(
		side_effect=ProductNotFoundError(product_id=str(product_id))
	)

	with pytest.raises(ProductNotFoundError):
		await product_service.delete(id=product_id)

	mock_product_repository.get.assert_awaited_once_with(product_id)


@pytest.mark.asyncio
async def test_delete_product_internal_error(
	product_service, mock_product_repository, sample_product
):
	mock_product_repository.get = AsyncMock(return_value=sample_product)
	mock_product_repository.delete = AsyncMock(side_effect=Exception('Ih! Deu ruim!'))

	with pytest.raises(ProductsInternalError) as exc_info:
		await product_service.delete(id=sample_product.id)

	assert 'Ih! Deu ruim!' in str(exc_info.value)
