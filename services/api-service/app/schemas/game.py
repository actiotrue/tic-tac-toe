import uuid

from app.models import GameResult, PlayerType
from app.schemas.base import CustomBaseModel
from app.schemas.player import PlayerSummary


class GamePlayerBase(CustomBaseModel):
    game_id: uuid.UUID
    player_id: uuid.UUID | None = None
    side: str
    type: PlayerType


class GamePlayerRead(GamePlayerBase):
    id: uuid.UUID
    player: PlayerSummary | None = None


class GamePlayerCreate(GamePlayerBase):
    pass


class GameBase(CustomBaseModel):
    id: uuid.UUID
    result: GameResult
    duration: int


class GameCreate(GameBase):
    players: list[GamePlayerCreate]


class GameRead(GameBase):
    players: list[GamePlayerRead]
