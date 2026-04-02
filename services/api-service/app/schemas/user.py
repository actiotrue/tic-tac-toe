import datetime
import uuid

from app.schemas.base import CustomBaseModel


class UserBase(CustomBaseModel):
    username: str


class UserReadWithoutPassword(UserBase):
    id: uuid.UUID


class UserRead(UserReadWithoutPassword):
    hashed_password: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UserRegister(UserBase):
    password: str


class UserCreate(UserBase):
    password: str


class UpdatePassword(CustomBaseModel):
    current_password: str
    new_password: str


class Token(CustomBaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: uuid.UUID
