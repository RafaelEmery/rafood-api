import psycopg2
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from src.core.config import settings
from src.core.deps import get_session
from src.main import app

# Since tests are not on Docker, we use localhost as DB host
# instead of 'database' (Docker service name)
TEST_DB_HOST = 'localhost'
TEST_DB_NAME = f'{settings.DB_NAME}_test'
TEST_DB_URL = (
	f'postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}'
	f'@{TEST_DB_HOST}:{settings.DB_PORT}/{TEST_DB_NAME}'
)


@pytest_asyncio.fixture(scope='session', autouse=True)
def create_test_db():
	"""
	Create the test database if it doesn't exists.
	Uses psycopg2 (sync connection) for that instead of asyncpg.
	"""
	conn = psycopg2.connect(
		dbname='postgres',
		user=settings.DB_USER,
		password=settings.DB_PASSWORD,
		host=TEST_DB_HOST,
		port=settings.DB_PORT,
	)
	conn.autocommit = True

	cur = conn.cursor()
	cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{TEST_DB_NAME}'")
	exists = cur.fetchone()

	if not exists:
		cur.execute(f'CREATE DATABASE "{TEST_DB_NAME}"')

	cur.close()
	conn.close()


@pytest_asyncio.fixture
async def session():
	"""
	Create a new database session for a test.
	First, creates an async engine and creates all tables.
	After the test, drops all tables and disposes the engine (drop_all).
	"""
	engine = create_async_engine(TEST_DB_URL, echo=False)

	async with engine.begin() as conn:
		await conn.run_sync(SQLModel.metadata.create_all)

	async_session = sessionmaker(
		bind=engine,
		class_=AsyncSession,
		autoflush=False,
		expire_on_commit=False,
	)

	async with async_session() as s:
		yield s

	async with engine.begin() as conn:
		await conn.run_sync(SQLModel.metadata.drop_all)

	await engine.dispose()


@pytest_asyncio.fixture
async def client(session):
	"""
	Create an HTTPX AsyncClient that uses the FastAPI app with
	an overridden get_session dependency to use the test session.
	"""

	async def override_get_session():
		yield session

	app.dependency_overrides[get_session] = override_get_session

	transport = ASGITransport(app=app)
	async with AsyncClient(transport=transport, base_url='http://testserver') as ac:
		yield ac

	app.dependency_overrides.clear()
