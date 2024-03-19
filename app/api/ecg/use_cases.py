from datetime import datetime
from typing import AsyncIterator

from fastapi import HTTPException

from app.db import AsyncSession
from app.models import ECG, ECGSchema


class UseCase:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session


class CreateECG(UseCase):
    async def execute(self, date: datetime) -> ECGSchema:
        async with self.async_session.begin() as session:
            ecg = await ECG.create(session, date)
            return ECGSchema.model_validate(ecg)


class ReadAllECG(UseCase):
    async def execute(self) -> AsyncIterator[ECGSchema]:
        async with self.async_session() as session:
            async for notebook in ECG.get_all(session, include_leads=True):
                yield ECGSchema.model_validate(notebook)


class ReadECG(UseCase):
    async def execute(self, ecg_id: int) -> ECGSchema:
        async with self.async_session() as session:
            notebook = await ECG.get_by_id(session, ecg_id, include_leads=True)
            if not notebook:
                raise HTTPException(status_code=404)
            return ECGSchema.model_validate(notebook)


class UpdateECG(UseCase):
    async def execute(self, ecg_id: int, date: datetime) -> ECGSchema:
        async with self.async_session.begin() as session:
            ecg = await ECG.get_by_id(session, ecg_id, include_leads=False)
            if not ecg:
                raise HTTPException(status_code=404)
            await ecg.update(session, date)
            await session.refresh(ecg)
            return ECGSchema.model_validate(ecg)


class DeleteECG(UseCase):
    async def execute(self, ecg_id: int) -> None:
        async with self.async_session.begin() as session:
            ecg = await ECG.get_by_id(session, ecg_id)
            if not ecg:
                return
            await ecg.delete(session)
