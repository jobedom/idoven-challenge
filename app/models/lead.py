from __future__ import annotations

from typing import TYPE_CHECKING, AsyncIterator

from sqlalchemy import JSON, ForeignKey, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, joinedload, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .ecg import ECG


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column("id", autoincrement=True, nullable=False, unique=True, primary_key=True)
    name: Mapped[str] = mapped_column("name", String, nullable=False)
    signal: Mapped[list[int]] = mapped_column("signal", JSON, nullable=False)

    ecg_id: Mapped[int] = mapped_column("ecg_id", ForeignKey("ecgs.id"), nullable=False)
    ecg: Mapped[ECG] = relationship("ECG", back_populates="leads")

    @classmethod
    async def get_all(cls, session: AsyncSession) -> AsyncIterator[Lead]:
        stmt = select(cls)
        stream = await session.stream_scalars(stmt.order_by(cls.id))
        async for row in stream:
            yield row

    @classmethod
    async def get_by_id(cls, session: AsyncSession, lead_id: int) -> Lead | None:
        stmt = select(cls).where(cls.id == lead_id)
        return await session.scalar(stmt.order_by(cls.id))

    @classmethod
    async def get_by_ids(cls, session: AsyncSession, lead_ids: list[int]) -> AsyncIterator[Lead]:
        stmt = select(cls).where(cls.id.in_(lead_ids)).options(joinedload(cls.ecg))  # type: ignore
        stream = await session.stream_scalars(stmt.order_by(cls.id))
        async for row in stream:
            yield row

    @classmethod
    async def create(cls, session: AsyncSession, ecg_id: int, name: str, signal: list[int]) -> ECG:
        lead = Lead(
            ecg_id=ecg_id,
            name=name,
            signal=signal,
        )
        session.add(lead)
        await session.flush()

        new = await cls.get_by_id(session, lead.id)
        if not new:
            raise RuntimeError()
        return new

    async def update(self, session: AsyncSession, name: str, signal: list[int]) -> None:
        self.name = name
        self.signal = signal
        await session.flush()

    async def delete(self, session: AsyncSession) -> None:
        await session.delete(self)
        await session.flush()
