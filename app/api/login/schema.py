from typing import Any

from pydantic import BaseModel


class LoginResponseSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayloadSchema(BaseModel):
    id: int
    email: str
    is_admin: bool


class TokenSchema(BaseModel):
    exp: int
    sub: dict[str, Any]
