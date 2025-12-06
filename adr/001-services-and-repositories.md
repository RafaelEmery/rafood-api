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

Using services and repositories instead of all in `api.py` files.

## Consequences

- More files and folders to manage
- More code to write
- Better separation of responsibilities
- Easier code reuse

## References

*Voices of my head and my experience*. There's a lot of articles about services, repositories, layers separation and others but i won't use any of these here.
