from pydantic import BaseModel

from app.models import UserSchema


class CreateUserRequest(BaseModel):
    email: str
    password: str
    is_admin: bool


class CreateUserResponse(UserSchema):
    pass


class ReadUserResponse(UserSchema):
    pass


class ReadAllUserResponse(BaseModel):
    users: list[UserSchema]
