from core.config import settings
import redis


redis_client = redis.Redis(
    host=settings.db_redis.REDIS_HOST,
    port=settings.db_redis.REDIS_PORT,
    db=1,
    password=settings.db_redis.REDIS_PASSWORD,
    decode_responses=True
)