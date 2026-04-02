import uuid
from asyncpg import Connection
from redis import Redis

from app.dao.uow import UnitOfWork
from app.models import Game, Player
from app.schemas.player import PlayerCreate, PlayerUpdate, PlayerWithRank


class PlayerService:
    def __init__(self, connection: Connection, redis_client: Redis):
        self.uow = UnitOfWork(connection, redis_client)

    async def get_all_players(self) -> list[Player]:
        async with self.uow as uow:
            return await uow.players.get_all()

    async def get_player_by_id(self, player_id: uuid.UUID) -> Player | None:
        async with self.uow as uow:
            return await uow.players.get_by_id(player_id)

    async def get_player_by_username(self, username: str) -> Player | None:
        async with self.uow as uow:
            return await uow.players.get_by_username(username)

    async def get_player_with_rank(self, player_id: uuid.UUID) -> PlayerWithRank | None:
        async with self.uow as uow:
            player = await uow.players.get_by_id(player_id)
            if not player:
                return None
            rank = await uow.leaderboard.get_player_rank(player_id)
            player_with_rank = PlayerWithRank(
                **player.to_dict(),
                rank=rank,
            )
            return player_with_rank

    async def create_player(self, player_in: PlayerCreate) -> Player:
        async with self.uow as uow:
            return await uow.players.create(player_in)

    async def update_player(
        self, player_id: uuid.UUID, player_in: PlayerUpdate
    ) -> Player:
        async with self.uow as uow:
            if player_in.username:
                await uow.users.update_username(player_id, player_in.username)
            return await uow.players.update(player_id, player_in)

    async def get_leaderboard(self, start: int, end: int) -> list[PlayerWithRank]:
        async with self.uow as uow:
            player_ids = await uow.leaderboard.get_all(start, end)
            if not player_ids:
                return []
            players = await uow.players.get_by_ids(player_ids)
            return [
                PlayerWithRank(**player.to_dict(), rank=start + index + 1)
                for index, player in enumerate(players)
            ]

    async def get_games_summary_by_player_id(
        self, player_id: uuid.UUID, limit: int, offset: int
    ) -> list[Game]:
        async with self.uow as uow:
            return await uow.games.get_games_summary_by_player_id(
                player_id, limit, offset
            )
