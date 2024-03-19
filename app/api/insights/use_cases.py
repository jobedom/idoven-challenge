from fastapi import HTTPException

from app.db import AsyncSession
from app.models import ECG, ECGSchema


class UseCase:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session


class ReadECG(UseCase):
    async def execute(self, ecg_id: int) -> ECGSchema:
        async with self.async_session() as session:
            ecg = await ECG.get_by_id(session, ecg_id)
            if not ecg:
                raise HTTPException(status_code=404)
            return ECGSchema.model_validate(ecg)
