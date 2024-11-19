import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    ALGORITHM: str
    SECRET_KEY: str
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str
    ADMIN_TELEGRAM_ID: int
    model_config = SettingsConfigDict(env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env"))


class Admin:
    def __init__(self, username, telegram_id, password):
        self.username = username
        self.telegram_id = telegram_id
        self.password = password


settings = Settings()

admin = Admin(
    username=settings.ADMIN_USERNAME,
    telegram_id=settings.ADMIN_TELEGRAM_ID,
    password=settings.ADMIN_PASSWORD
)


def get_db_url():
    return f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"


def get_secret_key():
    return settings.SECRET_KEY


def get_algorithm():
    return settings.ALGORITHM
