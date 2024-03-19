from typing import AsyncIterator

from fastapi import HTTPException

from app.db import AsyncSession
from app.models import ECG, Lead, LeadSchema


class UseCase:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session


class CreateLead(UseCase):
    async def execute(self, ecg_id: int, name: str, signal: list[int]) -> LeadSchema:
        async with self.async_session.begin() as session:
            ecg = await ECG.get_by_id(session, ecg_id)
            if not ecg:
                raise HTTPException(status_code=404)
            lead = await Lead.create(session, ecg_id, name, signal)
            return LeadSchema.model_validate(lead)


class ReadAllLead(UseCase):
    async def execute(self) -> AsyncIterator[LeadSchema]:
        async with self.async_session() as session:
            async for lead in Lead.get_all(session):
                yield LeadSchema.model_validate(lead)


class ReadLead(UseCase):
    async def execute(self, lead_id: int) -> LeadSchema:
        async with self.async_session() as session:
            lead = await Lead.get_by_id(session, lead_id)
            if not lead:
                raise HTTPException(status_code=404)
            return LeadSchema.model_validate(lead)


class UpdateLead(UseCase):
    async def execute(self, lead_id: int, ecg_id: int, title: str, content: str) -> LeadSchema:
        async with self.async_session.begin() as session:
            lead = await Lead.get_by_id(session, lead_id)
            if not lead:
                raise HTTPException(status_code=404)

            if lead.ecg_id != ecg_id:
                ecg = await ECG.get_by_id(session, ecg_id)
                if not ecg:
                    raise HTTPException(status_code=404)
                updated_ecg_id = ecg.id
            else:
                updated_ecg_id = lead.ecg_id

            await lead.update(session, updated_ecg_id, title, content)
            await session.refresh(lead)
            return LeadSchema.model_validate(lead)


class DeleteLead(UseCase):
    async def execute(self, lead_id: int) -> None:
        async with self.async_session.begin() as session:
            lead = await Lead.get_by_id(session, lead_id)
            if not lead:
                return
            await lead.delete(session)
