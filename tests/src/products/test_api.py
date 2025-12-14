from uuid import uuid4

import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_get_products(session, client, product_factory):
	product_factory(session, name='Everton Araujo')
	product_factory(session, name='Pedro')
	product_factory(session, name='Cebolinha')

	await session.commit()

	response = await client.get('/api/v1/products')
	data = response.json()

	assert response.status_code == status.HTTP_200_OK
	assert len(data) == 3


@pytest.mark.asyncio
async def test_get_products_filter_by_name(session, client, product_factory):
	expected_name = 'Saul'

	product_factory(session, name=expected_name)
	product_factory(session, name=expected_name)
	product_factory(session, name='Delacruz')

	await session.commit()

	response = await client.get(f'/api/v1/products?name={expected_name}')
	data = response.json()

	assert response.status_code == status.HTTP_200_OK
	assert len(data) == 2
	assert all(expected_name in product['name'] for product in data)


@pytest.mark.asyncio
async def test_get_products_filter_by_category_id(
	session, client, product_factory, category_factory
):
	first_category = category_factory(session, name='Filipe Luis')
	second_category = category_factory(session, name='Rodrigo Caio')

	product_factory(session, name='Diego Ribas', category_id=first_category.id)
	product_factory(session, name='Gabriel Barbosa', category_id=first_category.id)
	product_factory(session, name='João Gomes', category_id=second_category.id)

	await session.commit()

	response = await client.get(f'/api/v1/products?category_id={first_category.id}')
	data = response.json()

	assert response.status_code == status.HTTP_200_OK
	assert len(data) == 2
	assert all(str(product['category_id']) == str(first_category.id) for product in data)


@pytest.mark.asyncio
async def test_find_product_by_id(session, client, product_factory):
	product = product_factory(session, name='Michael', price=45.90)
	await session.commit()

	response = await client.get(f'/api/v1/products/{product.id}')
	data = response.json()

	assert response.status_code == status.HTTP_200_OK
	assert data['id'] == str(product.id)
	assert data['name'] == 'Michael'
	assert data['price'] == 45.90


@pytest.mark.asyncio
async def test_find_product_by_id_with_offers(session, client, product_factory, offer_factory):
	product = product_factory(session, name='Ibson', price=60.00)
	first_offer = offer_factory(session, product_id=product.id, price=10.0)
	second_offer = offer_factory(session, product_id=product.id, price=15.0)
	await session.commit()

	response = await client.get(f'/api/v1/products/{product.id}')
	data = response.json()
	offer_ids = [offer['id'] for offer in data['offers']]

	assert response.status_code == status.HTTP_200_OK
	assert data['id'] == str(product.id)
	assert data['name'] == 'Ibson'
	assert data['price'] == 60.00
	assert 'offers' in data
	assert len(data['offers']) == 2
	assert str(first_offer.id) in offer_ids
	assert str(second_offer.id) in offer_ids


@pytest.mark.asyncio
async def test_find_product_by_id_not_found_error(client):
	response = await client.get(f'/api/v1/products/{str(uuid4())}')

	assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_create_product(
	client, session, restaurant_factory, category_factory, build_create_payload
):
	restaurant = restaurant_factory(session, name='Jorge Jesus')
	category = category_factory(session, name='João de Deus')
	await session.commit()

	payload = build_create_payload(restaurant_id=restaurant.id, category_id=category.id)

	response = await client.post('/api/v1/products', json=payload)
	data = response.json()

	assert response.status_code == status.HTTP_201_CREATED
	assert data['id'] is not None


@pytest.mark.asyncio
@pytest.mark.parametrize(
	'payload_override',
	[
		{'name': ''},
		{'name': None},
		{'name': 123},
		{'price': -10},
		{'price': 'invalid'},
		{'price': None},
		{'price': ''},
		{'restaurant_id': None},
		{'restaurant_id': ''},
		{'restaurant_id': 'abcd-1234'},
		{'category_id': None},
		{'category_id': ''},
		{'category_id': 'abcd-1234'},
		{'image_url': 'invalid-url'},
		{'image_url': 123},
	],
)
async def test_create_product_bad_request_error(
	client, session, restaurant_factory, category_factory, build_create_payload, payload_override
):
	restaurant = restaurant_factory(session)
	category = category_factory(session)
	await session.commit()

	payload = build_create_payload(restaurant_id=restaurant.id, category_id=category.id)
	payload.update(payload_override)

	response = await client.post('/api/v1/products', json=payload)

	assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_update_product(client, session, product_factory, build_update_payload):
	product = product_factory(session, name='Ayrton Lucas', price=10.00)
	await session.commit()

	payload = build_update_payload(
		restaurant_id=product.restaurant_id,
		category_id=product.category_id,
	)

	response = await client.patch(f'/api/v1/products/{product.id}', json=payload)
	data = response.json()

	assert response.status_code == status.HTTP_200_OK
	assert data['name'] == 'Alex Sandro'
	assert data['price'] == 39.99


@pytest.mark.asyncio
async def test_update_product_not_found_error(
	client, session, product_factory, build_update_payload
):
	product = product_factory(session)
	await session.commit()

	payload = build_update_payload(
		restaurant_id=product.restaurant_id, category_id=product.category_id
	)

	response = await client.patch(f'/api/v1/products/{str(uuid4())}', json=payload)

	assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
@pytest.mark.parametrize(
	'payload_override',
	[
		{'name': ''},
		{'name': None},
		{'price': -10},
		{'price': 'invalid'},
		{'price': None},
		{'restaurant_id': None},
		{'restaurant_id': 'abcd-1234'},
		{'category_id': None},
		{'category_id': 'abcd-1234'},
		{'image_url': 'invalid-url'},
		{'image_url': 123},
	],
)
async def test_update_product_bad_request_error(
	client, session, product_factory, build_update_payload, payload_override
):
	product = product_factory(session, name='Vitinho')
	await session.commit()

	payload = build_update_payload(
		restaurant_id=product.restaurant_id, category_id=product.category_id
	)
	payload.update(payload_override)

	response = await client.patch(f'/api/v1/products/{product.id}', json=payload)

	assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_delete_product(client, session, product_factory):
	product = product_factory(session, name='Gerson')
	await session.commit()

	response = await client.delete(f'/api/v1/products/{product.id}')

	assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_delete_product_not_found_error(client):
	response = await client.delete(f'/api/v1/products/{str(uuid4())}')

	assert response.status_code == status.HTTP_404_NOT_FOUND
