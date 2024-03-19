from datetime import datetime
from typing import AsyncIterator

from fastapi import HTTPException

from app.db import AsyncSession
from app.models import ECG, ECGSchema, Lead


class UseCase:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session


class CreateECG(UseCase):
    async def execute(self, date: datetime, leads: list[Lead]) -> ECGSchema:
        async with self.async_session.begin() as session:
            ecg = await ECG.create(session, date, leads)
            return ECGSchema.model_validate(ecg)


class ReadAllECG(UseCase):
    async def execute(self) -> AsyncIterator[ECGSchema]:
        async with self.async_session() as session:
            async for ecg in ECG.get_all(session):
                yield ECGSchema.model_validate(ecg)


class ReadECG(UseCase):
    async def execute(self, ecg_id: int) -> ECGSchema:
        async with self.async_session() as session:
            ecg = await ECG.get_by_id(session, ecg_id)
            if not ecg:
                raise HTTPException(status_code=404)
            return ECGSchema.model_validate(ecg)


class DeleteECG(UseCase):
    async def execute(self, ecg_id: int) -> None:
        async with self.async_session.begin() as session:
            ecg = await ECG.get_by_id(session, ecg_id)
            if ecg:
                await ECG.delete(ecg, session)
