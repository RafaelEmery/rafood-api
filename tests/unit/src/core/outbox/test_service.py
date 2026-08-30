from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

from src.core.outbox.models import OutboxEvent
from src.core.outbox.repository import OutboxRepository
from src.core.outbox.service import OutboxService


@pytest.fixture
def mock_outbox_repository():
	return MagicMock(spec=OutboxRepository)


@pytest.fixture
def outbox_service(mock_outbox_repository):
	return OutboxService(mock_outbox_repository)


def _sample_outbox_event() -> OutboxEvent:
	return OutboxEvent(
		aggregatetype='product',
		aggregateid=str(uuid4()),
		type='ProductCreated',
		payload={'name': 'Pizza'},
	)


@patch('src.core.outbox.service.logger')
def test_create_outbox_event_success(mock_logger, outbox_service, mock_outbox_repository):
	event = _sample_outbox_event()

	outbox_service.create(event)

	mock_outbox_repository.add.assert_called_once_with(event)
	mock_logger.info.assert_called_once_with(
		'outbox_event_enqueued',
		outbox_event_id=str(event.id),
		aggregate_type=event.aggregatetype,
		aggregate_id=event.aggregateid,
		event_type=event.type,
	)
	mock_logger.exception.assert_not_called()


@patch('src.core.outbox.service.logger')
def test_create_outbox_event_failure(mock_logger, outbox_service, mock_outbox_repository):
	event = _sample_outbox_event()
	error = RuntimeError('outbox insert failed')
	mock_outbox_repository.add.side_effect = error

	with pytest.raises(RuntimeError, match='outbox insert failed'):
		outbox_service.create(event)

	mock_outbox_repository.add.assert_called_once_with(event)
	mock_logger.info.assert_not_called()
	mock_logger.exception.assert_called_once_with(
		'outbox_event_enqueue_failed',
		aggregate_type=event.aggregatetype,
		aggregate_id=event.aggregateid,
		event_type=event.type,
	)
