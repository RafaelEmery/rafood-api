from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession

from core.config import settings


db_url = f'postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}'
engine: AsyncEngine = create_async_engine(db_url)


Session: AsyncSession = sessionmaker(
	autocommit=False,
	autoflush=False,
	expire_on_commit=False,
	class_=AsyncSession,
	bind=engine,
)
