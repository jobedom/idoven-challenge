from typing import AsyncIterator

from fastapi import HTTPException

from app.db import AsyncSession
from app.lib.password import get_hashed_password
from app.models import User, UserSchema


class UseCase:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session


class CreateUser(UseCase):
    async def execute(self, email: str, password: str, is_admin: bool) -> UserSchema:
        async with self.async_session.begin() as session:
            hashed_password = get_hashed_password(password)
            user = await User.create(session, email, hashed_password, is_admin)
            return UserSchema.model_validate(user)


class ReadAllUsers(UseCase):
    async def execute(self) -> AsyncIterator[UserSchema]:
        async with self.async_session() as session:
            async for user in User.get_all(session):
                yield UserSchema.model_validate(user)


class ReadUser(UseCase):
    async def execute(self, user_id: int) -> UserSchema:
        async with self.async_session() as session:
            user = await User.get_by_id(session, user_id)
            if not user:
                raise HTTPException(status_code=404)
            return UserSchema.model_validate(user)


class ReadUserByEmail(UseCase):
    async def execute(self, email: str) -> UserSchema:
        async with self.async_session() as session:
            user = await User.get_by_email(session, email)
            if not user:
                return None
            return UserSchema.model_validate(user)


class DeleteUser(UseCase):
    async def execute(self, user_id: int) -> None:
        async with self.async_session.begin() as session:
            user = await User.get_by_id(session, user_id)
            if user:
                await User.delete(session, user)
