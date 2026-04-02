from datetime import timedelta
import uuid

import jwt
from app.core.security import create_token, get_password_hash, verify_password
from app.core.settings import settings


def test_get_password_hash():
    password = "password"
    hashed_password = get_password_hash(password)
    assert verify_password(password, hashed_password)


def test_get_password_hash_error():
    password = "password"
    hashed_password = get_password_hash(password)
    verifed, _ = verify_password(password + "1", hashed_password)
    assert not verifed


def test_create_access_token():
    subject = {"sub": str(uuid.uuid7()), "type": "access"}
    expires_delta = timedelta(minutes=10)
    access_token = create_token(subject, expires_delta)
    assert access_token

    payload = jwt.decode(
        access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    assert payload["sub"] == subject["sub"]
    assert payload["type"] == subject["type"]


def test_create_refresh_token():
    subject = {"sub": str(uuid.uuid7()), "type": "refresh"}
    expires_delta = timedelta(days=10)
    refresh_token = create_token(subject, expires_delta)
    assert refresh_token

    payload = jwt.decode(
        refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    assert payload["sub"] == subject["sub"]
    assert payload["type"] == subject["type"]
