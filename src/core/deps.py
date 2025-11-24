from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from core.database import Session


async def get_session() -> AsyncGenerator[AsyncSession, None]:
	"""
	Get an async session from the database.
	Starts a session, yields it and then closes it when it ends.
	"""
	session: AsyncSession = Session()

	try:
		yield session
	finally:
		await session.close()
