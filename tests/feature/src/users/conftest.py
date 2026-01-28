from uuid import uuid4

import pytest


@pytest.fixture
def build_create_payload():
	def _build():
		return {
			'first_name': 'Everton',
			'last_name': 'Cebolinha',
			'email': f'cebolinha_{uuid4()}@test.com',
			'password': 'cebooooola123',
		}

	return _build


@pytest.fixture
def build_update_payload():
	def _build():
		return {
			'first_name': 'Filipe',
			'last_name': 'Luis',
		}

	return _build
