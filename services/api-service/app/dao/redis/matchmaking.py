from app.dao.redis.base import RedisDaoBase


class MatchmakingDaoRedis(RedisDaoBase): ...


class PlayerDaoRedis(RedisDaoBase):
    async def get_leaderboard(self):
        pass
