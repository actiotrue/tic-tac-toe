from typing import Any

from fastapi import HTTPException


class AppError(Exception):
    pass


class EntityNotFound(AppError):
    def __init__(self, entity_name: str, entity_id: Any):
        self.entity_name = entity_name
        self.entity_id = entity_id


class InvalidGamePlayersError(AppError):
    pass


class DBError(AppError):
    pass


class TokenExpiredException(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Token expired")


class InvalidTokenException(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Invalid token")
