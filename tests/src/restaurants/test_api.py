from uuid import uuid4

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
async def test_find_restaurant_by_id(client, session, restaurant_factory):
	restaurant = restaurant_factory(session, name='Varela')
	await session.commit()

	response = await client.get(f'/api/v1/restaurants/{restaurant.id}')
	data = response.json()

	assert response.status_code == status.HTTP_200_OK
	assert data['id'] == str(restaurant.id)
	assert data['name'] == 'Varela'


@pytest.mark.asyncio
async def test_find_restaurant_by_id_not_found_error(client):
	response = await client.get(f'/api/v1/restaurants/{str(uuid4())}')

	assert response.status_code == status.HTTP_404_NOT_FOUND


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
		{'name': 123},
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


@pytest.mark.asyncio
async def test_update_restaurant(client, session, restaurant_factory, build_update_payload):
	restaurant = restaurant_factory(session, name='João Gomes')
	await session.commit()

	payload = build_update_payload(owner_id=restaurant.owner_id)

	response = await client.patch(f'/api/v1/restaurants/{restaurant.id}', json=payload)
	data = response.json()

	assert response.status_code == status.HTTP_200_OK
	assert data['name'] == 'Erick Pulgar'
	assert data['image_url'] == 'https://example.com/new-image.jpg'


@pytest.mark.asyncio
async def test_update_restaurant_not_found_error(
	client, session, restaurant_factory, build_update_payload
):
	restaurant = restaurant_factory(session, name='João Gomes')
	await session.commit()

	payload = build_update_payload(owner_id=restaurant.owner_id)

	response = await client.patch(f'/api/v1/restaurants/{str(uuid4())}', json=payload)

	assert response.status_code == status.HTTP_404_NOT_FOUND


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
async def test_update_restaurant_bad_request_error(
	client, session, restaurant_factory, build_update_payload, payload_override
):
	restaurant = restaurant_factory(session, name='João Gomes')
	await session.commit()

	payload = build_update_payload(owner_id=restaurant.owner_id)
	payload.update(payload_override)

	response = await client.patch(f'/api/v1/restaurants/{restaurant.id}', json=payload)

	assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_delete_restaurant(client, session, restaurant_factory):
	restaurant = restaurant_factory(session, name='To Be Deleted')
	await session.commit()

	response = await client.delete(f'/api/v1/restaurants/{restaurant.id}')

	assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_delete_restaurant_not_found_error(client):
	response = await client.delete(f'/api/v1/restaurants/{str(uuid4())}')

	assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_create_restaurant_schedules(
	client, session, restaurant_factory, build_schedule_create_payload
):
	restaurant = restaurant_factory(session, name='Léo Ortiz')
	await session.commit()

	payload = build_schedule_create_payload()

	response = await client.post(f'/api/v1/restaurants/{restaurant.id}/schedules', json=payload)
	data = response.json()

	assert response.status_code == status.HTTP_201_CREATED
	assert data['id'] is not None


@pytest.mark.asyncio
async def test_create_restaurant_schedules_not_found_error(
	client, session, restaurant_factory, build_schedule_create_payload
):
	"""Returns 500 because of FK constraint violation"""
	_ = restaurant_factory(session, name='Léo Pereira')
	await session.commit()

	payload = build_schedule_create_payload()

	response = await client.post(f'/api/v1/restaurants/{str(uuid4())}/schedules', json=payload)

	assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


@pytest.mark.asyncio
@pytest.mark.parametrize(
	'payload_override',
	[
		{'day_type': 'invalid-day-type'},
		{'day_type': None},
		{'start_day': 'invalid-start-day'},
		{'start_day': None},
		{'end_day': 'invalid-end-day'},
		{'end_day': None},
		{'start_time': '25:00:00'},
		{'start_time': None},
		{'end_time': 'ab:cd:ef'},
		{'end_time': None},
	],
)
async def test_create_restaurant_schedules_bad_request_error(
	client, session, restaurant_factory, build_schedule_create_payload, payload_override
):
	restaurant = restaurant_factory(session, name='Léo Pereira')
	await session.commit()

	payload = build_schedule_create_payload()
	payload.update(payload_override)

	response = await client.post(f'/api/v1/restaurants/{restaurant.id}/schedules', json=payload)

	assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_update_restaurant_schedule(
	client, session, restaurant_schedule_factory, build_schedule_update_payload
):
	schedule = restaurant_schedule_factory(session, day_type='weekday')
	await session.commit()

	payload = build_schedule_update_payload()

	response = await client.patch(
		f'/api/v1/restaurants/{schedule.restaurant_id}/schedules/{schedule.id}', json=payload
	)
	data = response.json()

	assert response.status_code == status.HTTP_200_OK
	assert data['day_type'] == 'weekday'
	assert data['start_day'] == 'monday'
	assert data['end_day'] == 'tuesday'
	assert data['start_time'] == '18:00:00'
	assert data['end_time'] == '23:00:00'


@pytest.mark.asyncio
async def test_update_restaurant_schedule_not_found_error(
	client, session, restaurant_schedule_factory, build_schedule_update_payload
):
	schedule = restaurant_schedule_factory(session, day_type='weekday')
	await session.commit()

	payload = build_schedule_update_payload()

	response = await client.patch(
		f'/api/v1/restaurants/{schedule.restaurant_id}/schedules/{str(uuid4())}', json=payload
	)

	assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_update_restaurant_schedule_restaurant_not_found_error(
	client, session, restaurant_schedule_factory, build_schedule_update_payload
):
	schedule = restaurant_schedule_factory(session, day_type='weekday')
	await session.commit()

	payload = build_schedule_update_payload()

	response = await client.patch(
		f'/api/v1/restaurants/{str(uuid4())}/schedules/{schedule.id}', json=payload
	)

	assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
@pytest.mark.parametrize(
	'payload_override',
	[
		{'day_type': 'invalid-day-type'},
		{'day_type': None},
		{'start_day': 'invalid-start-day'},
		{'start_day': None},
		{'end_day': 'invalid-end-day'},
		{'end_day': None},
		{'start_time': '25:00:00'},
		{'start_time': None},
		{'end_time': 'ab:cd:ef'},
		{'end_time': None},
	],
)
async def test_update_restaurant_schedule_bad_request_error(
	client, session, restaurant_schedule_factory, build_schedule_update_payload, payload_override
):
	schedule = restaurant_schedule_factory(session, day_type='weekday')
	await session.commit()

	payload = build_schedule_update_payload()
	payload.update(payload_override)

	response = await client.patch(
		f'/api/v1/restaurants/{schedule.restaurant_id}/schedules/{schedule.id}', json=payload
	)

	assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_delete_restaurant_schedule(client, session, restaurant_schedule_factory):
	schedule = restaurant_schedule_factory(session, day_type='weekday')
	await session.commit()

	response = await client.delete(
		f'/api/v1/restaurants/{schedule.restaurant_id}/schedules/{schedule.id}'
	)

	assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_delete_restaurant_schedule_not_found_error(
	client, session, restaurant_schedule_factory
):
	schedule = restaurant_schedule_factory(session, day_type='weekday')
	await session.commit()

	response = await client.delete(
		f'/api/v1/restaurants/{schedule.restaurant_id}/schedules/{str(uuid4())}'
	)

	assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_restaurant_schedule_restaurant_not_found_error(
	client, session, restaurant_schedule_factory
):
	schedule = restaurant_schedule_factory(session, day_type='weekday')
	await session.commit()

	response = await client.delete(f'/api/v1/restaurants/{str(uuid4())}/schedules/{schedule.id}')

	assert response.status_code == status.HTTP_404_NOT_FOUND
