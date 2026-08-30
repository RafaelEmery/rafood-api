from sqlalchemy.future import select

from src.core.outbox.models import OutboxEvent


async def fetch_outbox_events(session) -> list[OutboxEvent]:
	result = await session.execute(select(OutboxEvent))
	return list(result.scalars().all())
