from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.deps import get_session
from src.core.outbox.repository import OutboxRepository


def get_outbox_repository(db: AsyncSession = Depends(get_session)) -> OutboxRepository:
	return OutboxRepository(db)
