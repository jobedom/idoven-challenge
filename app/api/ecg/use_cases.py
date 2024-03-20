# pylint: disable=raise-missing-from

from datetime import datetime

from fastapi import HTTPException

from app.db import AsyncSession
from app.models import ECG, ECGSchema, LeadSchema, User


class UseCase:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session


class CreateECG(UseCase):
    async def execute(self, ecg_id: str, date: datetime, leads: list[LeadSchema], auth_user: User) -> ECGSchema:
        if auth_user.is_admin:
            raise HTTPException(status_code=403)
        async with self.async_session.begin() as session:
            ecg = await ECG.create(session, ecg_id, date, leads, auth_user)
            return ECGSchema.model_validate(ecg)


class ReadECG(UseCase):
    async def execute(self, ecg_id: str, auth_user: User) -> ECGSchema:
        if auth_user.is_admin:
            raise HTTPException(status_code=403)
        async with self.async_session() as session:
            ecg = await ECG.get_by_id(session, ecg_id, auth_user)
            if not ecg:
                raise HTTPException(status_code=404)
            return ECGSchema.model_validate(ecg)


class DeleteECG(UseCase):
    async def execute(self, ecg_id: str, auth_user: User) -> None:
        if auth_user.is_admin:
            raise HTTPException(status_code=403)
        async with self.async_session.begin() as session:
            ecg = await ECG.get_by_id(session, ecg_id, auth_user)
            if ecg:
                try:
                    await ECG.delete(session, ecg, auth_user)
                except AssertionError:
                    raise HTTPException(status_code=403)
            else:
                raise HTTPException(status_code=404)
