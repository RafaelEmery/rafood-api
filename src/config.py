from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "RaFood API"
    APP_DESCRIPTION: str = (
        "RESTful API to manage RaFood's restaurants, products and offers."
    )
    APP_VERSION: str = "1.0.0"
    APP_HOST: str
    APP_PORT: int

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
