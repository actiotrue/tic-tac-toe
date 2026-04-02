import uuid

from loguru import logger

from app.dao.postgres.base import SqlDaoBase
from app.exceptions import EntityNotFound
from app.models import GameResult, Player
from app.schemas.player import PlayerCreate, PlayerUpdate
from app.utils import generate_updated_fields


class PlayerDao(SqlDaoBase):
    """PlayerDao for crud operations on players"""

    async def create(self, player_in: PlayerCreate) -> Player:
        query = """INSERT INTO players (user_id, username, image_url) VALUES ($1, $2, $3) RETURNING *"""
        row = await self.db.fetchrow(
            query, player_in.user_id, player_in.username, player_in.image_url
        )
        player = Player.from_row(row)
        logger.info(f"Created player ID: {player.user_id} Username: {player.username}")
        return player

    async def get_by_id(self, player_id: uuid.UUID) -> Player | None:
        query = """SELECT * FROM players WHERE user_id = $1"""
        row = await self.db.fetchrow(query, player_id)
        if row is None:
            return None
        player = Player.from_row(row)
        logger.info(f"Found player ID: {player.user_id} Username: {player.username}")
        return player

    async def get_by_ids(self, player_ids: list[uuid.UUID]) -> list[Player]:
        query = """SELECT p.*
        FROM unnest($1::uuid[]) WITH ORDINALITY AS ord(id, pos)
        JOIN players p ON p.user_id = ord.id
        ORDER BY ord.pos"""
        rows = await self.db.fetch(query, player_ids)
        players = Player.from_rows(rows)
        logger.info(f"Found {len(players)} players")
        return players

    async def get_by_username(self, username: str) -> Player | None:
        query = """SELECT * FROM players WHERE username = $1"""
        row = await self.db.fetchrow(query, username)
        if row is None:
            return None
        player = Player.from_row(row)
        logger.info(f"Found player ID: {player.user_id} Username: {player.username}")
        return player

    async def get_all(self) -> list[Player]:
        query = """SELECT * FROM players"""
        rows = await self.db.fetch(query)
        players = [Player.from_row(row) for row in rows]
        logger.info(f"Found {len(players)} players")
        return players

    async def update(self, player_id: uuid.UUID, player_in: PlayerUpdate) -> Player:
        player_data = player_in.model_dump(exclude_unset=True)
        if not player_data:
            return await self.get_by_id(player_id)
        fileds = generate_updated_fields(player_data)
        values = list(player_data.values())
        values.append(player_id)

        query = f"UPDATE players SET {','.join(fileds)} WHERE user_id = ${len(values)} RETURNING *"
        row = await self.db.fetchrow(
            query,
            *values,
        )
        if row is None:
            raise EntityNotFound("Player", player_id)
        player = Player.from_row(row)
        return player

    async def update_stats(
        self, player_id: uuid.UUID, result: GameResult, new_rating: int, side: str
    ) -> None:
        query = """
        UPDATE players
        SET
            wins = wins + CASE 
                WHEN ($1 = 'x_won' AND $4 = 'X') OR ($1 = 'o_won' AND $4 = 'O') THEN 1 
                ELSE 0 END,
            
            losses = losses + CASE 
                WHEN ($1 = 'o_won' AND $4 = 'X') OR ($1 = 'x_won' AND $4 = 'O') THEN 1 
                ELSE 0 END,
                
            draws = draws + CASE WHEN $1 = 'draw' THEN 1 ELSE 0 END,
            rating = $2
        WHERE user_id = $3
        """
        await self.db.execute(query, new_rating, result, player_id, side)
