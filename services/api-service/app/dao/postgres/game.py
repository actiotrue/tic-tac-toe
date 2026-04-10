import uuid

from loguru import logger

from app.dao.postgres.base import SqlDaoBase
from app.models import Game, GamePlayer
from app.schemas.game import GameCreate, GamePlayerCreate
from app.exceptions import EntityNotFound

class GameDao(SqlDaoBase):
    """GameDao for crud operations on games"""

    async def get_all(self) -> list[Game]:
        query = """SELECT * FROM games"""
        rows = await self.db.fetch(query)
        games = [Game.from_row(row) for row in rows]
        logger.info(f"Found {len(games)} games")
        return games

    async def get_by_id(self, game_id: uuid.UUID) -> Game | None:
        query = """SELECT * FROM games WHERE id = $1"""
        row = await self.db.fetchrow(query, game_id)
        if row is None:
            return None
        game = Game.from_row(row)
        logger.info(f"Found game ID: {game.id}")
        return game

    async def create(self, game_in: GameCreate) -> Game:
        query = """INSERT INTO games (id, result, duration) 
        VALUES ($1, $2, $3) RETURNING *"""
        row = await self.db.fetchrow(
            query,
            game_in.id,
            game_in.result,
            game_in.duration,
        )
        if not row:
            raise EntityNotFound("Game", game_in.id)
        game = Game.from_row(row)
        logger.info(f"Created game ID: {game.id}")
        return game

    async def create_game_players(
        self, game_id: uuid.UUID, players: list[GamePlayerCreate]
    ) -> list[GamePlayer]:
        query = """
        INSERT INTO game_players (game_id, player_id, side, type) 
        VALUES ($1, $2, $3, $4)
        """
        data = [(game_id, p.player_id, p.side, p.type) for p in players]
        rows = await self.db.fetchmany(query, data)
        game_players = GamePlayer.from_rows(rows)
        logger.info(f"Created {len(players)} players for game ID: {game_id}")
        return game_players

    async def get_games_summary_by_player_id(
        self, player_id: uuid.UUID, limit: int = 10, offset: int = 0
    ) -> list[Game]:
        query = """
        SELECT
        g.id,
        g.duration,
        g.result,
        json_agg(
            json_build_object(
                'id', gp.id,
                'type', gp.type,
                'side', gp.side,
                'game_id', gp.game_id,
                'player_id', gp.player_id,
                'player',
                    CASE
                        WHEN p.user_id IS NULL THEN NULL
                        ELSE json_build_object(
                            'user_id', p.user_id,
                            'username', p.username,
                            'image_url', p.image_url
                        )
                    END
            )
        ) AS players
        FROM games g
        JOIN game_players gp
            ON gp.game_id = g.id
        LEFT JOIN players p
            ON p.user_id = gp.player_id
        WHERE EXISTS (
            SELECT 1
            FROM game_players gp2
            WHERE gp2.game_id = g.id
            AND gp2.player_id = $1
        )
        GROUP BY g.id
        ORDER BY g.created_at DESC
        LIMIT $2
        OFFSET $3
        """
        rows = await self.db.fetch(query, player_id, limit, offset)
        print(rows)
        games = Game.from_rows(rows)
        logger.info(f"Found {len(games)} games")
        return games
