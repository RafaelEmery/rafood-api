from datetime import datetime, time
from unittest.mock import patch
from uuid import uuid4

import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_list_offers(session, client, product_factory, offer_factory):
	product = product_factory(session, name='Pizza Especial')
	offer_factory(session, product_id=product.id, price=10.99)
	offer_factory(session, product_id=product.id, price=15.99)
	offer_factory(session, product_id=product.id, price=20.99)

	await session.commit()

	response = await client.get('/api/v1/offers')
	data = response.json()

	assert response.status_code == status.HTTP_200_OK
	assert len(data) == 3
	for item in data:
		assert 'product_id' not in item
		assert item['product']['id'] == str(product.id)
		assert item['product']['name'] == 'Pizza Especial'


@pytest.mark.asyncio
async def test_find_offer_by_id(session, client, offer_factory):
	offer = offer_factory(session, price=12.50, active=True)
	await session.commit()

	response = await client.get(f'/api/v1/offers/{offer.id}')
	data = response.json()

	assert response.status_code == status.HTTP_200_OK
	assert data['id'] == str(offer.id)
	assert data['price'] == 12.50
	assert data['active'] is True


@pytest.mark.asyncio
async def test_find_offer_by_id_not_found_error(client):
	response = await client.get(f'/api/v1/offers/{str(uuid4())}')

	assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_create_offer(client, session, product_factory, build_create_payload):
	product = product_factory(session, name='Pizza Especial')
	await session.commit()

	payload = build_create_payload(product_id=product.id)

	response = await client.post('/api/v1/offers', json=payload)
	data = response.json()

	assert response.status_code == status.HTTP_201_CREATED
	assert data['id'] is not None


@pytest.mark.asyncio
@pytest.mark.parametrize(
	'payload_override',
	[
		{'price': -10},
		{'price': 0},
		{'price': 'invalid'},
		{'price': None},
		{'product_id': None},
		{'product_id': ''},
		{'product_id': 'invalid-uuid'},
	],
)
async def test_create_offer_bad_request_error(
	client, session, product_factory, build_create_payload, payload_override
):
	product = product_factory(session)
	await session.commit()

	payload = build_create_payload(product_id=product.id)
	payload.update(payload_override)

	response = await client.post('/api/v1/offers', json=payload)

	assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_update_offer(client, session, offer_factory, build_update_payload):
	offer = offer_factory(session, price=10.00)
	await session.commit()

	payload = build_update_payload()

	response = await client.patch(f'/api/v1/offers/{offer.id}', json=payload)
	data = response.json()

	assert response.status_code == status.HTTP_200_OK
	assert data['price'] == 25.99
	assert data['active'] is True


@pytest.mark.asyncio
async def test_update_offer_not_found_error(client, build_update_payload):
	payload = build_update_payload()

	response = await client.patch(f'/api/v1/offers/{str(uuid4())}', json=payload)

	assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
@pytest.mark.parametrize(
	'payload_override',
	[
		{'price': -10, 'active': True},
		{'price': 0, 'active': True},
		{'price': 'invalid', 'active': True},
		{'price': None, 'active': True},
		{'price': 20.00, 'active': None},
		{'price': 20.00, 'active': 'invalid'},
		{'price': 20.00, 'active': 'Falsy'},
	],
)
async def test_update_offer_bad_request_error(
	client, session, offer_factory, build_update_payload, payload_override
):
	offer = offer_factory(session, price=15.00)
	await session.commit()

	payload = build_update_payload()
	payload.update(payload_override)

	response = await client.patch(f'/api/v1/offers/{offer.id}', json=payload)

	assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_delete_offer(client, session, offer_factory):
	offer = offer_factory(session, price=30.00)
	await session.commit()

	response = await client.delete(f'/api/v1/offers/{offer.id}')

	assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_delete_offer_not_found_error(client):
	response = await client.delete(f'/api/v1/offers/{str(uuid4())}')

	assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_create_offer_schedule(
	client, session, offer_factory, build_offer_schedule_create_payload
):
	offer = offer_factory(session, price=20.00)
	await session.commit()

	payload = build_offer_schedule_create_payload()

	response = await client.post(f'/api/v1/offers/{offer.id}/schedules', json=payload)
	data = response.json()

	assert response.status_code == status.HTTP_201_CREATED
	assert data['id'] is not None


@pytest.mark.asyncio
async def test_create_offer_schedule_not_found_error(client, build_offer_schedule_create_payload):
	payload = build_offer_schedule_create_payload()

	response = await client.post(f'/api/v1/offers/{str(uuid4())}/schedules', json=payload)

	assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
@pytest.mark.parametrize(
	'payload_override',
	[
		{'day': 'invalid-day'},
		{'day': None},
		{'start_time': '25:00:00'},
		{'start_time': 'invalid'},
		{'start_time': None},
		{'end_time': '25:00:00'},
		{'end_time': 'invalid'},
		{'end_time': None},
		{'repeats': None},
		{'repeats': 'invalid'},
	],
)
async def test_create_offer_schedule_bad_request_error(
	client, session, offer_factory, build_offer_schedule_create_payload, payload_override
):
	offer = offer_factory(session)
	await session.commit()

	payload = build_offer_schedule_create_payload()
	payload.update(payload_override)

	response = await client.post(f'/api/v1/offers/{offer.id}/schedules', json=payload)

	assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_update_offer_schedule(
	client, session, offer_schedule_factory, build_offer_schedule_update_payload
):
	schedule = offer_schedule_factory(session, day='monday', repeats=True)
	await session.commit()

	payload = build_offer_schedule_update_payload()

	response = await client.patch(
		f'/api/v1/offers/{schedule.offer_id}/schedules/{schedule.id}', json=payload
	)
	data = response.json()

	assert response.status_code == status.HTTP_200_OK
	assert data['day'] == 'friday'
	assert data['start_time'] == '12:00:00'
	assert data['end_time'] == '20:00:00'
	assert data['repeats'] is False


@pytest.mark.asyncio
async def test_update_offer_schedule_not_found_error(
	client, session, offer_schedule_factory, build_offer_schedule_update_payload
):
	schedule = offer_schedule_factory(session)
	await session.commit()

	payload = build_offer_schedule_update_payload()

	response = await client.patch(
		f'/api/v1/offers/{schedule.offer_id}/schedules/{str(uuid4())}', json=payload
	)

	assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_update_offer_schedule_offer_not_found_error(
	client, session, offer_schedule_factory, build_offer_schedule_update_payload
):
	schedule = offer_schedule_factory(session)
	await session.commit()

	payload = build_offer_schedule_update_payload()

	response = await client.patch(
		f'/api/v1/offers/{str(uuid4())}/schedules/{schedule.id}', json=payload
	)

	assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
@pytest.mark.parametrize(
	'payload_override',
	[
		{'day': 'invalid-day'},
		{'day': None},
		{'start_time': '25:00:00'},
		{'start_time': 'invalid'},
		{'start_time': None},
		{'end_time': '25:00:00'},
		{'end_time': 'invalid'},
		{'end_time': None},
		{'repeats': None},
		{'repeats': 'invalid'},
	],
)
async def test_update_offer_schedule_bad_request_error(
	client, session, offer_schedule_factory, build_offer_schedule_update_payload, payload_override
):
	schedule = offer_schedule_factory(session)
	await session.commit()

	payload = build_offer_schedule_update_payload()
	payload.update(payload_override)

	response = await client.patch(
		f'/api/v1/offers/{schedule.offer_id}/schedules/{schedule.id}', json=payload
	)

	assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_delete_offer_schedule(client, session, offer_schedule_factory):
	schedule = offer_schedule_factory(session)
	await session.commit()

	response = await client.delete(f'/api/v1/offers/{schedule.offer_id}/schedules/{schedule.id}')

	assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_delete_offer_schedule_not_found_error(client, session, offer_schedule_factory):
	schedule = offer_schedule_factory(session)
	await session.commit()

	response = await client.delete(f'/api/v1/offers/{schedule.offer_id}/schedules/{str(uuid4())}')

	assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_offer_schedule_offer_not_found_error(client, session, offer_schedule_factory):
	schedule = offer_schedule_factory(session)
	await session.commit()

	response = await client.delete(f'/api/v1/offers/{str(uuid4())}/schedules/{schedule.id}')

	assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_list_active_offers_near_by_success(
	client,
	session,
	restaurant_factory,
	product_factory,
	offer_factory,
	offer_schedule_factory,
	active_near_by_reference_time,
):
	restaurant = restaurant_factory(session, latitude=-23.5505, longitude=-46.6333)
	product = product_factory(session, restaurant_id=restaurant.id)
	offer = offer_factory(session, product_id=product.id, active=True)
	offer_schedule_factory(
		session,
		offer_id=offer.id,
		day='tuesday',
		start_time=time(9, 0),
		end_time=time(18, 0),
	)
	await session.commit()

	response = await client.get(
		'/api/v1/offers/active',
		params={'latitude': -23.5505, 'longitude': -46.6333, 'radius': 1000},
	)

	data = response.json()
	assert response.status_code == status.HTTP_200_OK
	assert len(data) == 1
	assert data[0]['id'] == str(offer.id)
	assert data[0]['active'] is True
	assert 'product_id' not in data[0]
	assert data[0]['product']['id'] == str(product.id)
	assert data[0]['product']['name'] == product.name


@pytest.mark.asyncio
async def test_list_active_offers_near_by_inactive_offer_excluded(
	client,
	session,
	restaurant_factory,
	product_factory,
	offer_factory,
	offer_schedule_factory,
	active_near_by_reference_time,
):
	restaurant = restaurant_factory(session, latitude=-23.5505, longitude=-46.6333)
	product = product_factory(session, restaurant_id=restaurant.id)
	offer = offer_factory(session, product_id=product.id, active=False)
	offer_schedule_factory(
		session,
		offer_id=offer.id,
		day='tuesday',
		start_time=time(9, 0),
		end_time=time(18, 0),
	)
	await session.commit()

	response = await client.get(
		'/api/v1/offers/active',
		params={'latitude': -23.5505, 'longitude': -46.6333, 'radius': 1000},
	)

	assert response.status_code == status.HTTP_200_OK
	assert response.json() == []


@pytest.mark.asyncio
async def test_list_active_offers_near_by_outside_radius(
	client,
	session,
	restaurant_factory,
	product_factory,
	offer_factory,
	offer_schedule_factory,
	active_near_by_reference_time,
):
	restaurant = restaurant_factory(session, latitude=-22.9068, longitude=-43.1729)
	product = product_factory(session, restaurant_id=restaurant.id)
	offer = offer_factory(session, product_id=product.id, active=True)
	offer_schedule_factory(
		session,
		offer_id=offer.id,
		day='tuesday',
		start_time=time(9, 0),
		end_time=time(18, 0),
	)
	await session.commit()

	response = await client.get(
		'/api/v1/offers/active',
		params={'latitude': -23.5505, 'longitude': -46.6333, 'radius': 1000},
	)

	assert response.status_code == status.HTTP_200_OK
	assert response.json() == []


@pytest.mark.asyncio
async def test_list_active_offers_near_by_closed_schedule(
	client,
	session,
	restaurant_factory,
	product_factory,
	offer_factory,
	offer_schedule_factory,
):
	restaurant = restaurant_factory(session, latitude=-23.5505, longitude=-46.6333)
	product = product_factory(session, restaurant_id=restaurant.id)
	offer = offer_factory(session, product_id=product.id, active=True)
	offer_schedule_factory(
		session,
		offer_id=offer.id,
		day='tuesday',
		start_time=time(9, 0),
		end_time=time(18, 0),
	)
	await session.commit()

	with patch('src.offers.repository.datetime') as mock_datetime:
		mock_datetime.now.return_value = datetime(2026, 5, 19, 20, 0)
		response = await client.get(
			'/api/v1/offers/active',
			params={'latitude': -23.5505, 'longitude': -46.6333, 'radius': 1000},
		)

	assert response.status_code == status.HTTP_200_OK
	assert response.json() == []


@pytest.mark.asyncio
async def test_list_active_offers_near_by_wrong_day_excluded(
	client,
	session,
	restaurant_factory,
	product_factory,
	offer_factory,
	offer_schedule_factory,
	active_near_by_reference_time,
):
	restaurant = restaurant_factory(session, latitude=-23.5505, longitude=-46.6333)
	product = product_factory(session, restaurant_id=restaurant.id)
	offer = offer_factory(session, product_id=product.id, active=True)
	offer_schedule_factory(
		session,
		offer_id=offer.id,
		day='monday',
		start_time=time(9, 0),
		end_time=time(18, 0),
	)
	await session.commit()

	response = await client.get(
		'/api/v1/offers/active',
		params={'latitude': -23.5505, 'longitude': -46.6333, 'radius': 1000},
	)

	assert response.status_code == status.HTTP_200_OK
	assert response.json() == []


@pytest.mark.asyncio
async def test_list_active_offers_near_by_default_radius(
	client,
	session,
	restaurant_factory,
	product_factory,
	offer_factory,
	offer_schedule_factory,
	active_near_by_reference_time,
):
	restaurant = restaurant_factory(session, latitude=-23.5615, longitude=-46.6559)
	product = product_factory(session, restaurant_id=restaurant.id)
	offer = offer_factory(session, product_id=product.id, active=True)
	offer_schedule_factory(
		session,
		offer_id=offer.id,
		day='tuesday',
		start_time=time(9, 0),
		end_time=time(18, 0),
	)
	await session.commit()

	response = await client.get(
		'/api/v1/offers/active',
		params={'latitude': -23.5505, 'longitude': -46.6333},
	)

	data = response.json()
	assert response.status_code == status.HTTP_200_OK
	assert len(data) == 1
	assert data[0]['id'] == str(offer.id)


@pytest.mark.asyncio
@pytest.mark.parametrize(
	'missing_param',
	['latitude', 'longitude'],
)
async def test_list_active_offers_near_by_missing_coordinates(client, missing_param):
	params = {'latitude': -23.5505, 'longitude': -46.6333, 'radius': 1000}
	params.pop(missing_param)

	response = await client.get('/api/v1/offers/active', params=params)

	assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
