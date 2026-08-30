from src.core.logging.logger import StructLogger
from src.core.outbox.models import OutboxEvent
from src.core.outbox.repository import OutboxRepository

logger = StructLogger()


class OutboxService:
	repository: OutboxRepository

	def __init__(self, repository: OutboxRepository) -> None:
		self.repository = repository

	def create(self, event: OutboxEvent) -> None:
		try:
			self.repository.add(event)

			logger.info(
				'Outbox event enqueued',
				outbox_event_id=str(event.id),
				aggregate_type=event.aggregatetype,
				aggregate_id=event.aggregateid,
				event_type=event.type,
			)
		except Exception:
			logger.exception(
				'Outbox event enqueue failed',
				aggregate_type=event.aggregatetype,
				aggregate_id=event.aggregateid,
				event_type=event.type,
			)
			raise
