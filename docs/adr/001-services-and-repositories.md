# Services and repositories

## Context

Actually it's all on endpoint functions like:

```python
@router.get(
	'',
	name='List offers',
	status_code=status.HTTP_200_OK,
	description='Get all offers',
	response_model=list[OfferSchema],
)
async def list_offers(db: AsyncSession = Depends(get_session)):
	async with db as session:
		try:
			result = await session.execute(select(Offer))
			offers: list[OfferSchema] = result.scalars().unique().all()

			return offers
		except Exception as e:
			raise HTTPException(
				status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
			) from e
```

Leads to a lot of code and make code reuse way more difficult. We don't have many responsibilities separation too.

## Decision

Using services and repositories instead of all in `api.py` files. The code will be more like:

```python
# api.py
@router.get(
	'',
	name='List products',
	status_code=status.HTTP_200_OK,
	response_model=list[ProductWithCategoriesSchema],
)
async def list_products(
	name: str | None = None,
	category_id: UUID | None = None,
	service: ProductServiceDeps = None,
):
	try:
		return await service.list(name, category_id)
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


# service.py
class ProductService:
	repository: ProductRepository

	def __init__(self, repository: ProductRepository):
		self.repository = repository

	async def list(
		self, name: str | None, category_id: UUID | None
	) -> list[ProductWithCategoriesSchema]:
		return await self.repository.list(name, category_id)


# repository.py
class ProductRepository:
	db: AsyncSession

	def __init__(self, db: AsyncSession):
		self.db = db

	async def list(self, name: str | None, category_id: UUID | None) -> list[Product]:
		query = select(Product)

		if name is not None:
			query = query.filter(Product.name.like(f'%{name}%'))
		if category_id is not None:
			query = query.filter(Product.category_id == category_id)

		result = await self.db.execute(query)

		return result.scalars().unique().all()
```

And the dependency injection (DI) is by `deps.py`:

```python
def get_product_repository(
	db: AsyncSession = Depends(get_session),
) -> ProductRepository:
	return ProductRepository(db)


def get_product_service(
	repository: ProductRepository = Depends(get_product_repository),
) -> ProductService:
	return ProductService(repository)


ProductServiceDeps = Annotated[ProductService, Depends(get_product_service)]
```

## Consequences

- More files and folders to manage
- More code to write
- Better separation of responsibilities
- Easier code reuse

## References

*Voices of my head and my experience*. There's a lot of articles about services, repositories, layers separation and others but i won't use any of these here.
