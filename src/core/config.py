from pydantic_settings import BaseSettings


class Settings(BaseSettings):
	APP_NAME: str = 'RaFood API'
	APP_DESCRIPTION: str = "RESTful API to manage RaFood's restaurants, products and offers."
	APP_VERSION: str = '1.0.0'
	APP_V1_PREFIX: str = '/api/v1'
	APP_HOST: str = 'localhost'
	APP_PORT: int = 8000

	LOG_LEVEL: str = 'INFO'
	LOG_JSON_FORMAT: bool = True  # Use JSON format for logs (ideal for production)
	LOG_NAME: str = 'rafood-api'  # Application logs name
	LOG_ACCESS_NAME: str = (
		'rafood-api-access'  # Uvicorn access logs, re-emitted using structured information
	)
	LOGS_CORRELATION_HEADER_NAME: str = 'X-Request-ID'

	DB_USER: str = 'postgres'
	DB_PASSWORD: str = ''
	DB_HOST: str = 'localhost'
	DB_NAME: str = 'rafood_db'
	DB_PORT: int = 5432

	class Config:
		case_sensitive = True  # Environment variables are case sensitive
		env_file = '.env'  # Load environment variables from .env file
		extra = 'ignore'  # Ignore extra environment variables


settings = Settings()
