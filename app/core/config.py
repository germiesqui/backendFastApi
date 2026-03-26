import logging

from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_server: str
    postgres_port: int
    postgres_db: str
    redis_host: str
    redis_port: int

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    def get_db_url(self):
        return (f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_server}:{self.postgres_port}/{self.postgres_db}")



try:
    settings = Settings()
except ValidationError as e:
    logger.fatal(f"Error de validación en el .env: {e}")
    exit(1)