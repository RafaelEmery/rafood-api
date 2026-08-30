from sqlalchemy.ext.asyncio import AsyncSession

from src.core.outbox.models import OutboxEvent


class OutboxRepository:
	def __init__(self, db: AsyncSession) -> None:
		self.db = db

	def add(self, event: OutboxEvent) -> None:
		self.db.add(event)
