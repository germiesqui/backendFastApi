import logging

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.core.config import settings

logger = logging.getLogger(__name__)

try:
    db_url = settings.get_db_url()
    engine = create_async_engine(db_url)
    logger.info(f"Conexion con BDD creada")
except Exception as e:
    logger.fatal(f"Postgres: Error de conexión -> {e}")
    exit(1)


async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with async_session_maker() as session:
        yield session