import pytest


@pytest.mark.asyncio
async def test_ping(client):
	response = await client.get('/ping')

	data = response.json()

	assert response.status_code == 200
	assert data['message'] == 'pong'
