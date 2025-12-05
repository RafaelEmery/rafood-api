from datetime import time
from uuid import uuid4

import pytest

from src.offers.models import Offer, OfferSchedule


@pytest.fixture
def offer_factory(product_factory):
	def create(session, **kwargs):
		# Create product if not provided
		if 'product_id' not in kwargs:
			product = product_factory(session)
			kwargs['product_id'] = product.id

		obj = Offer(
			id=uuid4(),
			product_id=kwargs['product_id'],
			price=kwargs.get('price', 19.99),
		)
		session.add(obj)

		return obj

	return create


@pytest.fixture
def offer_schedule_factory(offer_factory):
	def create(session, **kwargs):
		# Create offer if not provided
		if 'offer_id' not in kwargs:
			offer = offer_factory(session)
			kwargs['offer_id'] = offer.id

		obj = OfferSchedule(
			id=uuid4(),
			offer_id=kwargs['offer_id'],
			day=kwargs.get('day', 'monday'),
			start_time=kwargs.get('start_time', time(9, 0)),
			end_time=kwargs.get('end_time', time(18, 0)),
			repeats=kwargs.get('repeats', False),
		)
		session.add(obj)

		return obj

	return create


@pytest.fixture
def build_create_payload():
	def _build(product_id=None):
		return {
			'product_id': str(product_id) if product_id else str(uuid4()),
			'price': 15.99,
		}

	return _build


@pytest.fixture
def build_update_payload():
	def _build():
		return {
			'price': 25.99,
		}

	return _build


@pytest.fixture
def build_offer_schedule_create_payload():
	def _build():
		return {
			'day': 'monday',
			'start_time': '10:00:00',
			'end_time': '22:00:00',
			'repeats': True,
		}

	return _build


@pytest.fixture
def build_offer_schedule_update_payload():
	def _build():
		return {
			'day': 'friday',
			'start_time': '12:00:00',
			'end_time': '20:00:00',
			'repeats': False,
		}

	return _build
