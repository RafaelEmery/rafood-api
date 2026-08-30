from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.deps import get_session
from src.core.outbox.repository import OutboxRepository
from src.core.outbox.service import OutboxService


def get_outbox_repository(db: AsyncSession = Depends(get_session)) -> OutboxRepository:
	return OutboxRepository(db)


def get_outbox_service(
	repository: OutboxRepository = Depends(get_outbox_repository),
) -> OutboxService:
	return OutboxService(repository)


OutboxServiceDeps = Annotated[OutboxService, Depends(get_outbox_service)]
