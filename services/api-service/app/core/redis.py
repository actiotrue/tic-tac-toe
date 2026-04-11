from redis.asyncio import Redis, ConnectionPool
from app.core.settings import settings


pool = ConnectionPool.from_url(settings.redis_url, decode_responses=True)

redis_client = Redis(connection_pool=pool)
