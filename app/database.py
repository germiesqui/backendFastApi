from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import ValidationError

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
    print(f"❌ Error de validación en el .env: {e}")
    exit(1)

try:
    db_url = settings.get_db_url()
    engine = create_async_engine(db_url)
except Exception as e:
    print(f"❌ Postgres: Error de conexión -> {e}")
    exit(1)


async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with async_session_maker() as session:
        yield session