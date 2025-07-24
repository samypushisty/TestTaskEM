from core.config import settings
import redis
import redis.asyncio as redis_async
from contextlib import asynccontextmanager


redis_client = redis.Redis(
    host=settings.db_redis.REDIS_HOST,
    port=settings.db_redis.REDIS_PORT,
    db=1,
    password=settings.db_redis.REDIS_PASSWORD,
    decode_responses=True
)

async_redis_client = redis_async.Redis(
    host=settings.db_redis.REDIS_HOST,
    port=settings.db_redis.REDIS_PORT,
    db=1,
    password=settings.db_redis.REDIS_PASSWORD,
    decode_responses=True
)

@asynccontextmanager
async def redis_session_getter():
    async with async_redis_client as session:
        yield session