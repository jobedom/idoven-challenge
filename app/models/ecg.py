from __future__ import annotations

import datetime

from sqlalchemy import JSON, DateTime, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .schema import LeadSchema
from .user import User


class ECG(Base):
    __tablename__ = "ecgs"

    id: Mapped[int] = mapped_column("id", autoincrement=True, nullable=False, unique=True, primary_key=True)
    date: Mapped[datetime.datetime] = mapped_column("date", DateTime, nullable=False)
    leads: Mapped[list[LeadSchema]] = mapped_column("leads", JSON, nullable=False, default=list)

    owner_id: Mapped[int] = mapped_column("owner_id", nullable=False)

    @classmethod
    async def get_by_id(cls, session: AsyncSession, ecg_id: int, auth_user: User) -> ECG | None:
        stmt = select(cls).where(cls.id == ecg_id, cls.owner_id == auth_user.id)
        return await session.scalar(stmt.order_by(cls.id))

    @classmethod
    async def create(
        cls, session: AsyncSession, date: datetime.datetime, leads: list[LeadSchema], auth_user: User
    ) -> ECG:
        ecg = ECG(date=date, leads=leads, owner_id=auth_user.id)
        session.add(ecg)
        await session.flush()

        new = await cls.get_by_id(session, ecg.id, auth_user)
        if not new:
            raise RuntimeError()
        return new

    @classmethod
    async def delete(cls, session: AsyncSession, ecg: ECG, auth_user: User) -> None:
        if auth_user.is_admin or auth_user.id == ecg.owner_id:
            await session.delete(ecg)
            await session.flush()
        else:
            raise RuntimeError
