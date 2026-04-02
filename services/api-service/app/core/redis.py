from redis.asyncio import Redis, ConnectionPool
from app.core.settings import settings


pool = ConnectionPool.from_url(settings.REDIS_URL, decode_responses=True)

redis_client = Redis(connection_pool=pool)
