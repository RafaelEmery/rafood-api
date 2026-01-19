from uuid import uuid4

import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_list_users(session, client, user_factory):
	user_factory(session, first_name='Gabigol', last_name='Barbosa')
	user_factory(session, first_name='Pedro', last_name='Guilherme')
	user_factory(session, first_name='Giorgian', last_name='De Arrascaeta')

	await session.commit()

	response = await client.get('/api/v1/users')
	data = response.json()

	assert response.status_code == status.HTTP_200_OK
	assert len(data) == 3


@pytest.mark.asyncio
async def test_find_user_by_id(session, client, user_factory):
	user = user_factory(session, first_name='Bruno', last_name='Henrique', email='bruno@test.com')
	await session.commit()

	response = await client.get(f'/api/v1/users/{user.id}')
	data = response.json()

	assert response.status_code == status.HTTP_200_OK
	assert data['id'] == str(user.id)
	assert data['first_name'] == 'Bruno'
	assert data['last_name'] == 'Henrique'
	assert data['email'] == 'bruno@test.com'
	assert data['restaurants'] == []


@pytest.mark.asyncio
async def test_find_user_by_id_with_restaurants(session, client, user_factory, restaurant_factory):
	user = user_factory(session, first_name='Ronaldo', last_name='Angelim')
	first_restaurant = restaurant_factory(session, name='Ninho', owner_id=user.id)
	second_restaurant = restaurant_factory(session, name='Do Urubu', owner_id=user.id)
	await session.commit()

	response = await client.get(f'/api/v1/users/{user.id}')
	data = response.json()
	restaurant_ids = {r['id'] for r in data['restaurants']}
	restaurant_names = {r['name'] for r in data['restaurants']}

	assert response.status_code == status.HTTP_200_OK
	assert data['id'] == str(user.id)
	assert data['first_name'] == 'Ronaldo'
	assert data['last_name'] == 'Angelim'
	assert len(data['restaurants']) == 2

	assert str(first_restaurant.id) in restaurant_ids
	assert str(second_restaurant.id) in restaurant_ids
	assert 'Ninho' in restaurant_names
	assert 'Do Urubu' in restaurant_names


@pytest.mark.asyncio
async def test_find_user_by_id_not_found_error(client):
	response = await client.get(f'/api/v1/users/{str(uuid4())}')

	assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_create_user(client, build_create_payload):
	payload = build_create_payload()

	response = await client.post('/api/v1/users', json=payload)
	data = response.json()

	assert response.status_code == status.HTTP_201_CREATED
	assert data['id'] is not None


@pytest.mark.asyncio
@pytest.mark.parametrize(
	'payload_override',
	[
		{'first_name': ''},
		{'first_name': None},
		{'first_name': 123},
		{'last_name': ''},
		{'last_name': None},
		{'last_name': 123},
		{'email': ''},
		{'email': None},
		{'email': 'invalid-email'},
		{'email': 123},
		{'password': ''},
		{'password': None},
		{'password': 123},
	],
)
async def test_create_user_bad_request_error(client, build_create_payload, payload_override):
	payload = build_create_payload()
	payload.update(payload_override)

	response = await client.post('/api/v1/users', json=payload)

	assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_update_user(client, session, user_factory, build_update_payload):
	user = user_factory(session, first_name='Everton', last_name='Ribeiro')
	await session.commit()

	payload = build_update_payload()

	response = await client.put(f'/api/v1/users/{user.id}', json=payload)
	data = response.json()

	assert response.status_code == status.HTTP_200_OK
	assert data['first_name'] == 'Filipe'
	assert data['last_name'] == 'Luis'


@pytest.mark.asyncio
async def test_update_user_not_found_error(client, build_update_payload):
	payload = build_update_payload()

	response = await client.put(f'/api/v1/users/{str(uuid4())}', json=payload)

	assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
@pytest.mark.parametrize(
	'payload_override',
	[
		{'first_name': ''},
		{'first_name': None},
		{'first_name': 123},
		{'last_name': ''},
		{'last_name': None},
		{'last_name': 123},
	],
)
async def test_update_user_bad_request_error(
	client, session, user_factory, build_update_payload, payload_override
):
	user = user_factory(session, first_name='Diego', last_name='Alves')
	await session.commit()

	payload = build_update_payload()
	payload.update(payload_override)

	response = await client.put(f'/api/v1/users/{user.id}', json=payload)

	assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_delete_user(client, session, user_factory):
	user = user_factory(session, first_name='Rodrigo', last_name='Caio')
	await session.commit()

	response = await client.delete(f'/api/v1/users/{user.id}')

	assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_delete_user_not_found_error(client):
	response = await client.delete(f'/api/v1/users/{str(uuid4())}')

	assert response.status_code == status.HTTP_404_NOT_FOUND
