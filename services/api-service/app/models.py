from dataclasses import dataclass, field
import datetime
from enum import Enum
from typing import Optional
import uuid

from app.core.base_model import DBModel


class GameResult(str, Enum):
    X_WIN = "x_won"
    DRAW = "draw"
    O_WIN = "o_won"


class PlayerType(str, Enum):
    HUMAN = "human"
    AI = "ai"


@dataclass(slots=True)
class User(DBModel):
    id: uuid.UUID
    username: str
    hashed_password: str
    updated_at: Optional[datetime.datetime] = None
    created_at: Optional[datetime.datetime] = None


@dataclass(slots=True)
class Player(DBModel):
    user_id: uuid.UUID
    username: str
    image_url: str
    rating: int
    losses: int
    wins: int
    draws: int
    updated_at: Optional[datetime.datetime] = None
    created_at: Optional[datetime.datetime] = None

    games: list["Game"] = field(default_factory=list)


# Not actualy DBModel, need to fix
@dataclass(slots=True)
class PlayerSummary(DBModel):
    user_id: uuid.UUID
    username: str
    image_url: str


@dataclass(slots=True)
class Game(DBModel):
    id: uuid.UUID
    result: GameResult
    duration: int
    created_at: Optional[datetime.datetime] = None

    players: list["GamePlayer"] = field(default_factory=list)


@dataclass(slots=True)
class GamePlayer(DBModel):
    id: uuid.UUID
    game_id: uuid.UUID
    side: str
    type: PlayerType
    player_id: Optional[uuid.UUID] = None
    created_at: Optional[datetime.datetime] = None

    player: Optional[PlayerSummary] = None
