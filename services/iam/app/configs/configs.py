from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "iam"
    SERVICE_PORT: int = 8001

    # Database
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DB_HOST: str = "postgres"
    DB_PORT: int = 5432

    # JWT
    JWT_SECRET_KEY: str = "supersecret"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    class Config:
        env_file = ".env"

settings = Settings()
