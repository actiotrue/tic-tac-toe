import datetime
import uuid

from app.schemas.base import CustomBaseModel


class PlayerBase(CustomBaseModel):
    username: str
    image_url: str


class PlayerCreate(PlayerBase):
    user_id: uuid.UUID


class PlayerUpdate(CustomBaseModel):
    username: str | None = None
    image_url: str | None = None
    rating: int | None = None
    draws: int | None = None
    losses: int | None = None
    wins: int | None = None


class PlayerRead(PlayerBase):
    user_id: uuid.UUID
    rating: int
    draws: int
    losses: int
    wins: int
    created_at: datetime.datetime
    updated_at: datetime.datetime


class PlayerSummary(PlayerBase):
    user_id: uuid.UUID


class PlayerWithRank(PlayerRead):
    rank: int | None = None
