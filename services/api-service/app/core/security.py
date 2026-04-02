from datetime import datetime, timedelta, timezone
from typing import Any
from pwdlib import PasswordHash
import jwt

from app.core.settings import settings
from app.exceptions import InvalidTokenException, TokenExpiredException


password_hash = PasswordHash.recommended()


def verify_password(
    plain_password: str, hashed_password: str
) -> tuple[bool, str | None]:
    return password_hash.verify_and_update(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


def create_token(subject: dict[str, Any], expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, **subject}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def validate_token(token: str, token_type: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
    except jwt.PyJWTError:
        raise InvalidTokenException
    except jwt.ExpiredSignatureError:
        raise TokenExpiredException
    if payload.get("type") != token_type:
        raise InvalidTokenException
    return payload
