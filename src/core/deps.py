from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db.database import Session
from src.core.db.unit_of_work import UnitOfWork


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


def get_unit_of_work(db: AsyncSession = Depends(get_session)) -> UnitOfWork:
	return UnitOfWork(db)
