from redis import Redis

from app.dao.redis.key_schema import KeySchema


class RedisDaoBase:
    def __init__(self, redis_client: Redis, key_schema: KeySchema | None = None):
        self.redis = redis_client
        if key_schema is None:
            key_schema = KeySchema()
        self.key_schema = key_schema
