from fastapi import FastAPI

from config import settings


app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION
)


@app.get(
    '/ok',
    tags=['Standard'],
    status_code=200,
    name='Health Check Endpoint',
    description='Check if the API is running.'
)
async def ok():
    return {'message': 'OK!'}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True, log_level='info')