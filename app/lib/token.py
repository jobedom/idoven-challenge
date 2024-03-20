from datetime import datetime, timedelta, timezone
from typing import Any, Union

from jose import jwt

from app.settings import settings


def _create_token(
    subject: Union[str, Any], token_expire_minutes: int, secret_key: str, expires_delta: int = None
) -> str:
    now = datetime.now(timezone.utc)
    if expires_delta is not None:
        expires_delta = now + expires_delta
    else:
        expires_delta = now + timedelta(minutes=token_expire_minutes)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, secret_key, settings.TOKEN_ALGORITHM)
    return encoded_jwt


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    return _create_token(subject, settings.ACCESS_TOKEN_EXPIRE_MINUTES, settings.JWT_SECRET_KEY, expires_delta)


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    return _create_token(subject, settings.REFRESH_TOKEN_EXPIRE_MINUTES, settings.JWT_REFRESH_SECRET_KEY, expires_delta)
