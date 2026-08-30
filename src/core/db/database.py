from sqlalchemy.ext.asyncio import (
	AsyncEngine,
	AsyncSession,
	async_sessionmaker,
	create_async_engine,
)

from src.core.config import settings

db_url = f'postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}'
engine: AsyncEngine = create_async_engine(db_url)


Session = async_sessionmaker(
	autocommit=False,
	autoflush=False,
	expire_on_commit=False,
	class_=AsyncSession,
	bind=engine,
)
