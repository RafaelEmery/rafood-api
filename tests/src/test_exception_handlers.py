from uuid import uuid4

import pytest
from fastapi import status

from src.exceptions import NOT_FOUND_ERROR


@pytest.mark.asyncio
async def test_handled_app_internal_server_error(session, client, category_factory):
	"""Forcing a IntegrityError on categories API to return an app 500 error example"""
	category_factory(session, name='Filipe Luis')
	response = await client.post('/api/v1/categories', json={'name': 'Filipe Luis'})

	data = response.json()

	assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
	assert data['title'] == 'Internal Server Error'
	assert data['error'] == 'categories_internal_error'
	assert 'IntegrityError' in data['message']
	assert data['path'] == '/api/v1/categories'
	assert data['params'] is None
	assert data['query'] is None
	assert data['timestamp'] is not None


@pytest.mark.asyncio
async def test_handled_app_not_found_error(client):
	"""Forcing a not found on categories API to return an app 404 error example (simplified)"""
	category_id = str(uuid4())
	response = await client.delete(f'/api/v1/categories/{category_id}')
	data = response.json()

	assert response.status_code == status.HTTP_404_NOT_FOUND
	assert data['title'] == NOT_FOUND_ERROR
	assert data['error'] == 'category_not_found'
	assert data['message'] == f'Category {category_id} not found'
	assert data['timestamp'] is not None
	assert 'path' not in data
	assert 'params' not in data
	assert 'query' not in data
