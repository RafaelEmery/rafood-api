from uuid import uuid4

import pytest
from fastapi import status
from sqlalchemy.future import select

from src.categories.models import Category


@pytest.mark.asyncio
async def test_get_categories(client, session, category_factory):
	category_factory(session, name='Pizza')
	category_factory(session, name='Drinks')

	await session.commit()

	response = await client.get('/api/v1/categories')

	data = response.json()

	assert response.status_code == status.HTTP_200_OK
	assert len(data) == 2
	assert data[0]['name'] in ['Pizza', 'Drinks']


@pytest.mark.asyncio
async def test_create_category(client):
	payload = {'name': 'Burgers'}

	response = await client.post('/api/v1/categories', json=payload)

	data = response.json()

	assert response.status_code == status.HTTP_201_CREATED
	assert data['id'] is not None


@pytest.mark.parametrize(
	'payload',
	[
		{'name': ''},
		{'name': None},
		{'name': 123456},
		{'name': 0.0},
	],
)
@pytest.mark.asyncio
async def test_create_category_bad_request_error(client, payload):
	response = await client.post('/api/v1/categories', json=payload)

	assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_delete_category(client, session, category_factory):
	category = category_factory(session, name='Sushi')

	await session.commit()

	response = await client.delete(f'/api/v1/categories/{category.id}')

	result = await session.execute(select(Category).where(Category.id == category.id))
	deleted_category = result.scalars().first()

	assert response.status_code == status.HTTP_204_NO_CONTENT
	assert deleted_category is None


@pytest.mark.asyncio
async def test_delete_category_not_found_error(client):
	response = await client.delete(f'/api/v1/categories/{str(uuid4())}')

	assert response.status_code == status.HTTP_404_NOT_FOUND
