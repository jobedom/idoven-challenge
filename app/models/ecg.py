from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, AsyncIterator

from sqlalchemy import DateTime, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship, selectinload

from .base import Base

if TYPE_CHECKING:
    from .lead import Lead


class ECG(Base):
    __tablename__ = "ecgs"

    id: Mapped[int] = mapped_column("id", autoincrement=True, nullable=False, unique=True, primary_key=True)
    date: Mapped[datetime.datetime] = mapped_column("date", DateTime, nullable=False)

    leads: Mapped[list[Lead]] = relationship(
        "Lead",
        back_populates="ecg",
        order_by="Lead.id",
        cascade="save-update, merge, refresh-expire, expunge, delete, delete-orphan",
    )

    @classmethod
    async def get_all(cls, session: AsyncSession, include_leads: bool = True) -> AsyncIterator[ECG]:
        stmt = select(cls)
        if include_leads:
            stmt = stmt.options(selectinload(cls.leads))
        stream = await session.stream_scalars(stmt.order_by(cls.id))
        async for row in stream:
            yield row

    @classmethod
    async def get_by_id(cls, session: AsyncSession, notebook_id: int, include_leads: bool = True) -> ECG | None:
        stmt = select(cls).where(cls.id == notebook_id)
        if include_leads:
            stmt = stmt.options(selectinload(cls.leads))
        return await session.scalar(stmt.order_by(cls.id))

    @classmethod
    async def create(cls, session: AsyncSession, date: datetime.datetime) -> ECG:
        ecg = ECG(date=date)
        session.add(ecg)
        await session.flush()

        new = await cls.get_by_id(session, ecg.id, include_leads=True)
        if not new:
            raise RuntimeError()
        return new

    async def update(self, session: AsyncSession, date: datetime.datetime) -> None:
        self.date = date
        await session.flush()

    async def delete(self, session: AsyncSession) -> None:
        await session.delete(self)
        await session.flush()
