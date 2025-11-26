import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_get_restaurants(session, client, restaurant_factory):
	restaurant_factory(session, name='Arrascaeta')
	restaurant_factory(session, name='Bruno Henrique')
	restaurant_factory(session, name='Carrascal')

	await session.commit()

	response = await client.get('/api/v1/restaurants')
	data = response.json()

	assert response.status_code == 200
	assert len(data) == 3


@pytest.mark.asyncio
async def test_get_restaurants_filter_by_name(session, client, restaurant_factory):
	restaurant_factory(session, name='Arrascaeta')
	restaurant_factory(session, name='Bruno Henrique')
	restaurant_factory(session, name='Carrascal')

	await session.commit()

	response = await client.get('/api/v1/restaurants?name=Bruno')
	data = response.json()

	assert response.status_code == status.HTTP_200_OK
	assert len(data) == 1
	assert data[0]['name'] == 'Bruno Henrique'


@pytest.mark.asyncio
async def test_get_restaurants_filter_by_owner_id(
	session, client, restaurant_factory, user_factory
):
	first_owner = user_factory(session, email='filipe@test.com')
	second_owner = user_factory(session, email='luis@test.com')

	restaurant_factory(session, name='Arrascaeta', owner_id=first_owner.id)
	restaurant_factory(session, name='Bruno Henrique', owner_id=second_owner.id)
	restaurant_factory(session, name='Carrascal', owner_id=first_owner.id)

	await session.commit()

	response = await client.get(f'/api/v1/restaurants?owner_id={first_owner.id}')
	data = response.json()

	assert response.status_code == status.HTTP_200_OK
	assert len(data) == 2
	assert all(str(restaurant['owner_id']) == str(first_owner.id) for restaurant in data)


@pytest.mark.asyncio
async def test_create_restaurant(client, session, user_factory, build_create_payload):
	owner = user_factory(session, email='pulgar@test.com')
	await session.commit()

	payload = build_create_payload(owner_id=owner.id)

	response = await client.post('/api/v1/restaurants', json=payload)
	data = response.json()

	assert response.status_code == status.HTTP_201_CREATED
	assert data['id'] is not None


@pytest.mark.asyncio
@pytest.mark.parametrize(
	'payload_override',
	[
		{'name': ''},
		{'name': None},
		{'image_url': 'invalid-url'},
		{'image_url': 123},
		{'owner_id': None},
		{'street': ''},
		{'street': None},
		{'number': -5},
		{'number': 'abc'},
		{'number': None},
		{'neighborhood': ''},
		{'neighborhood': 123},
		{'neighborhood': None},
		{'city': ''},
		{'city': 123},
		{'city': None},
		{'state_abbr': 'XYZ'},
		{'state_abbr': 123},
		{'state_abbr': None},
	],
)
async def test_create_restaurant_bad_request_error(
	client, session, user_factory, build_create_payload, payload_override
):
	owner = user_factory(session, email=f'owner_{id(payload_override)}@test.com')
	await session.commit()

	payload = build_create_payload(owner_id=owner.id)
	payload.update(payload_override)

	response = await client.post('/api/v1/restaurants', json=payload)

	assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
