import logging
from uuid import UUID
from fastapi import FastAPI
from redis.asyncio import Redis
import json
from functools import wraps
from fastapi.encoders import jsonable_encoder

from app.core.config import settings

logger = logging.getLogger(__name__)

class RedisManager:
    def __init__(self):
        self.client: Redis | None = None

    async def init(self, host: str, port: int):
        logger.info(f"Cliente de Redis iniciado")
        self.client = Redis(host=host, port=port, decode_responses=True)

    async def close(self):
        if self.client:
            logger.info(f"Cliente de Redis detenido")
            await self.client.close()

redis_manager = RedisManager()

# Decorador
def cache_response(key_func, ttl=300):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = key_func(*args, **kwargs)

            cached = None
            try:
                cached = await __get_cache(key)
            except Exception as e:
                logger.error(f"Error en Redis (get): {e}")
            if cached:
                return json.loads(cached)
            
            result = await func(*args, **kwargs)
            try:
                encoded_result = jsonable_encoder(result)
                await __set_cache(key, json.dumps(encoded_result), ttl)
            except Exception as e:
                logger.error(f"Error en Redis (set): {e}")
            return result
        return wrapper
    return decorator


async def lifespan(app: FastAPI):
    await redis_manager.init(host=settings.redis_host, port=settings.redis_port)
    yield
    await redis_manager.close()

async def __get_cache(key: str):
    if not redis_manager.client:
        logger.error(f"Redis no inicializado")
        raise RuntimeError("Redis no inicializado")
    return await redis_manager.client.get(key)

async def __set_cache(key: str, value: str, ttl: int = 300):
    if not redis_manager.client:
        logger.error(f"Redis no inicializado")
        raise RuntimeError("Redis no inicializado")
    await redis_manager.client.set(key, value, ex=ttl)

async def __delete_cache(key: str):
    if not redis_manager.client:
        logger.error(f"Redis no inicializado")
        raise RuntimeError("Redis no inicializado")
    await redis_manager.client.delete(key)



def cache_player_by_id_key(player_id: UUID, **kwargs):
    return f"player:{player_id}"

def cache_player_by_username_key(username: str, **kwargs):
    return f"player:{username}"

async def invalidate_player_cache(player_id: UUID, username: str = None):
    await __delete_cache(f"player:id:{player_id}")
    if username:
        await __delete_cache(f"player:name:{username}")