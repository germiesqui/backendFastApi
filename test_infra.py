import redis
import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
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

try:
    settings = Settings()
except ValidationError as e:
    print(f"❌ Error de validación en el .env: {e}")
    exit(1)

def test_redis():
    try:
        r = redis.Redis(
            host=settings.redis_host, 
            port=settings.redis_port, 
            decode_responses=True
        )
        r.set("engine_status", "Aetheria Engine Online")
        value = r.get("engine_status")
        print(f"✅ Redis: Conexión exitosa. Valor recuperado: '{value}'")
    except Exception as e:
        print(f"❌ Redis: Error de conexión -> {e}")

async def async_text_postreSQL():
    try:
        db_url = f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_server}:{settings.postgres_port}/{settings.postgres_db}"
        engine = create_async_engine(db_url)
        
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1"))
            print(f"✅ Postgres: Conexión exitosa. Resultado del test: {result.fetchone()[0]}")
            await engine.dispose()
    except Exception as e:
        print(f"❌ Postgres: Error de conexión -> {e}")

print("--- Iniciando Test de Infraestructura ---")
test_redis()
asyncio.run(async_text_postreSQL())
print("--- Fin Test de Infraestructura ---")




