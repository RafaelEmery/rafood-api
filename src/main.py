from fastapi import FastAPI

from src.api import api_router
from src.core.config import settings
from src.core.exception_handlers import register_exception_handlers

app = FastAPI(
	title=settings.APP_NAME,
	description=settings.APP_DESCRIPTION,
	version=settings.APP_VERSION,
)
app.include_router(api_router, prefix=settings.APP_V1_PREFIX)
register_exception_handlers(app)


@app.get(
	'/ping',
	tags=['Standard'],
	status_code=200,
	name='Health Check Endpoint',
	description='Check if the API is running.',
)
async def ok():
	return {'message': 'pong'}


if __name__ == '__main__':
	import uvicorn

	uvicorn.run(
		'src.main:app',
		host=settings.APP_HOST,
		port=settings.APP_PORT,
		reload=True,
		log_level='info',
	)
