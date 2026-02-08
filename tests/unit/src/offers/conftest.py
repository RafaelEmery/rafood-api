from datetime import datetime, time
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from src.offers.models import Offer, OfferSchedule
from src.offers.repository import OfferRepository, OfferScheduleRepository
from src.offers.schemas import OfferWithSchedulesSchema
from src.offers.service import OfferScheduleService, OfferService


@pytest.fixture
def mock_offer_repository():
	return MagicMock(spec=OfferRepository)


@pytest.fixture
def mock_schedule_repository():
	return MagicMock(spec=OfferScheduleRepository)


@pytest.fixture
def offer_service(mock_offer_repository):
	return OfferService(repository=mock_offer_repository)


@pytest.fixture
def schedule_service(mock_schedule_repository, mock_offer_repository):
	return OfferScheduleService(
		repository=mock_schedule_repository, offer_repository=mock_offer_repository
	)


@pytest.fixture
def sample_offer():
	offer_id = uuid4()
	product_id = uuid4()
	return Offer(
		id=offer_id,
		product_id=product_id,
		price=10.0,
		active=True,
		created_at=datetime.now(),
		updated_at=datetime.now(),
	)


@pytest.fixture
def sample_offer_with_schedules(sample_offer):
	return OfferWithSchedulesSchema(
		id=sample_offer.id,
		product_id=sample_offer.product_id,
		price=sample_offer.price,
		active=sample_offer.active,
		schedules=[],
		created_at=sample_offer.created_at,
		updated_at=sample_offer.updated_at,
	)


@pytest.fixture
def sample_schedule():
	return OfferSchedule(
		id=uuid4(),
		offer_id=uuid4(),
		day='monday',
		start_time=time(8, 0, 0),
		end_time=time(18, 0, 0),
		repeats=False,
		created_at=datetime.now(),
		updated_at=datetime.now(),
	)
