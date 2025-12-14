from uuid import uuid4

import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_list_offers(session, client, offer_factory):
	offer_factory(session, price=10.99)
	offer_factory(session, price=15.99)
	offer_factory(session, price=20.99)

	await session.commit()

	response = await client.get('/api/v1/offers')
	data = response.json()

	assert response.status_code == status.HTTP_200_OK
	assert len(data) == 3


@pytest.mark.asyncio
async def test_find_offer_by_id(session, client, offer_factory):
	offer = offer_factory(session, price=12.50, active=True)
	await session.commit()

	response = await client.get(f'/api/v1/offers/{offer.id}')
	data = response.json()

	assert response.status_code == status.HTTP_200_OK
	assert data['id'] == str(offer.id)
	assert data['price'] == 12.50
	assert data['active'] == True


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
