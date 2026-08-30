from sqlalchemy.ext.asyncio import AsyncSession


class UnitOfWork:
	"""
	Owns the transaction boundary for a request: commit or rollback.

	Repositories only stage changes (add / flush / delete) on the shared
	AsyncSession; they must not commit. The service decides when the unit of
	work succeeds and calls commit, or rolls back on failure.

	Typical use: keep a domain write and a transactional outbox row in the
	same Postgres transaction.

	"If the Repository pattern is our abstraction over the idea of persistent
	storage, the Unit of Work (UoW) pattern is our abstraction over the idea
	of atomic operations. It will allow us to finally and fully decouple our
	service layer from the data layer."

	External reference: https://www.cosmicpython.com/book/chapter_06_uow
	"""

	def __init__(self, session: AsyncSession) -> None:
		self.session = session

	async def commit(self) -> None:
		await self.session.commit()

	async def rollback(self) -> None:
		await self.session.rollback()
