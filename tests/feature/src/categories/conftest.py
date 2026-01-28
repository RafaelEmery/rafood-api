import pytest


@pytest.fixture
def build_category_create_payload():
	def _build():
		return {'name': 'Burgers'}

	return _build
