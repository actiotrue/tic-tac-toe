import uuid

from app.dao.redis.base import RedisDaoBase


class LeaderboardDao(RedisDaoBase):
    async def create(self, player_id: uuid.UUID) -> None:
        """Create a new player in the leaderboard"""
        await self.redis.zadd(self.key_schema.leaderboard_key(), {str(player_id): 1000})

    async def get_all(self, start: int = 0, end: int = 10) -> list[uuid.UUID]:
        """Find all users with the highest score in the leaderboard"""
        player_ids_list = await self.redis.zrevrange(
            self.key_schema.leaderboard_key(), start, end - 1
        )
        player_ids = [uuid.UUID(player_id) for player_id in player_ids_list]
        return player_ids

    async def update_rating(self, player_id: uuid.UUID, new_score: int) -> None:
        """Update the rating of a player in the leaderboard"""
        await self.redis.zadd(
            self.key_schema.leaderboard_key(), {str(player_id): new_score}
        )

    async def get_player_rank(self, player_id: uuid.UUID) -> int | None:
        """Get the rank of a player in the leaderboard"""
        rank = await self.redis.zrevrank(
            self.key_schema.leaderboard_key(), str(player_id)
        )
        if rank is None:
            return None
        return int(rank) + 1

    async def delete(self, player_id: uuid.UUID) -> None:
        """Delete a player from the leaderboard"""
        await self.redis.zrem(self.key_schema.leaderboard_key(), str(player_id))
