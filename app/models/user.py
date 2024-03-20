from __future__ import annotations

from typing import AsyncIterator

from sqlalchemy import Boolean, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from app.lib.password import get_hashed_password

from .base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column("id", autoincrement=True, nullable=False, unique=True, primary_key=True)
    email: Mapped[str] = mapped_column("email", nullable=False, unique=True, primary_key=True)
    password: Mapped[str] = mapped_column("password", String, nullable=False)
    is_admin: Mapped[bool] = mapped_column("is_admin", Boolean, nullable=False, default=False)

    @classmethod
    async def get_all(cls, session: AsyncSession) -> AsyncIterator[User]:
        stmt = select(cls)
        stream = await session.stream_scalars(stmt.order_by(cls.id))
        async for row in stream:
            yield row

    @classmethod
    async def check_login(cls, session: AsyncSession, email: str, password: str) -> User | None:
        user = cls.get_by_email(session, email)
        if not user or user.password == get_hashed_password(password):
            return None
        return User

    @classmethod
    async def get_by_email(cls, session: AsyncSession, email: str) -> User | None:
        stmt = select(cls).where(cls.email == email)
        return await session.scalar(stmt.order_by(cls.email))

    @classmethod
    async def get_by_id(cls, session: AsyncSession, user_id: int) -> User | None:
        stmt = select(cls).where(cls.id == user_id)
        return await session.scalar(stmt.order_by(cls.id))

    @classmethod
    async def create(cls, session: AsyncSession, email: str, password: str, is_admin: bool = False) -> User:
        user = User(email=email, password=password, is_admin=is_admin)
        session.add(user)
        await session.flush()

        new = await cls.get_by_email(session, email)
        if not new:
            raise RuntimeError()
        return new

    @classmethod
    async def delete(cls, session: AsyncSession, user: User) -> None:
        await session.delete(user)
        await session.flush()
