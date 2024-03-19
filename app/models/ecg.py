from __future__ import annotations

import datetime
from typing import AsyncIterator

from sqlalchemy import JSON, DateTime, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .lead import Lead


class ECG(Base):
    __tablename__ = "ecgs"

    id: Mapped[int] = mapped_column("id", autoincrement=True, nullable=False, unique=True, primary_key=True)
    date: Mapped[datetime.datetime] = mapped_column("date", DateTime, nullable=False)
    leads: Mapped[list[Lead]] = mapped_column("leads", JSON, nullable=False, default=list)

    @classmethod
    async def get_all(cls, session: AsyncSession) -> AsyncIterator[ECG]:
        stmt = select(cls)
        stream = await session.stream_scalars(stmt.order_by(cls.id))
        async for row in stream:
            yield row

    @classmethod
    async def get_by_id(cls, session: AsyncSession, notebook_id: int) -> ECG | None:
        stmt = select(cls).where(cls.id == notebook_id)
        return await session.scalar(stmt.order_by(cls.id))

    @classmethod
    async def create(cls, session: AsyncSession, date: datetime.datetime, leads: list[Lead]) -> ECG:
        ecg = ECG(date=date, leads=leads)
        session.add(ecg)
        await session.flush()

        new = await cls.get_by_id(session, ecg.id)
        if not new:
            raise RuntimeError()
        return new

    @classmethod
    async def delete(cls, session: AsyncSession, ecg: ECG) -> None:
        await session.delete(ecg)
        await session.flush()
