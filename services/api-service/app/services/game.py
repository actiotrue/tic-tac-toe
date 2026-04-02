import uuid

from asyncpg import Connection
from redis import Redis

from app.dao.uow import UnitOfWork
from app.exceptions import InvalidGamePlayersError
from app.models import Game
from app.schemas.game import GameCreate
from app.utils import calculate_rating


class GameService:
    def __init__(self, connection: Connection, redis_client: Redis):
        self.uow = UnitOfWork(connection, redis_client)

    async def get_all_games(self) -> list[Game]:
        async with self.uow as uow:
            return await uow.games.get_all()

    async def get_game_by_id(self, game_id: uuid.UUID) -> Game | None:
        async with self.uow as uow:
            return await uow.games.get_by_id(game_id)

    async def create_game(self, game_in: GameCreate) -> Game:
        async with self.uow as uow:
            game = await uow.games.create(game_in)
            await uow.games.create_game_players(game.id, game_in.players)

            player_ids = [
                p.player_id for p in game_in.players if p.player_id is not None
            ]
            if len(player_ids) < 1:
                raise InvalidGamePlayersError
            players = await uow.players.get_by_ids(player_ids)

            side_map = {
                p.player_id: p.side for p in game_in.players if p.player_id is not None
            }

            for player in players:
                side = side_map[player.user_id]
                new_rating = calculate_rating(
                    current_rating=player.rating, result=game_in.result, side=side
                )
                await uow.players.update_stats(
                    player.user_id, new_rating, game_in.result, side
                )
        for player in players:
            side = side_map[player.user_id]
            new_rating = calculate_rating(
                current_rating=player.rating, result=game_in.result, side=side
            )
            await uow.leaderboard.update_rating(player.user_id, new_rating)
        return game
