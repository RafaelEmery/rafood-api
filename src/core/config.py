from pydantic_settings import BaseSettings


class Settings(BaseSettings):
	APP_NAME: str = 'RaFood API'
	APP_DESCRIPTION: str = "RESTful API to manage RaFood's restaurants, products and offers."
	APP_VERSION: str = '1.0.0'
	APP_V1_PREFIX: str = '/api/v1'
	APP_HOST: str
	APP_PORT: int

	DB_USER: str
	DB_PASSWORD: str
	DB_HOST: str
	DB_NAME: str
	DB_PORT: int

	class Config:
		case_sensitive = True  # Environment variables are case sensitive
		env_file = '.env'  # Load environment variables from .env file
		extra = 'ignore'  # Ignore extra environment variables


settings = Settings()
