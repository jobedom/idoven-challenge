# pylint: disable=unused-argument

from fastapi import APIRouter, Depends, Path, Request

from app.models import LeadSchema

from .schema import (
    CreateLeadRequest,
    CreateLeadResponse,
    ReadAllLeadResponse,
    ReadLeadResponse,
    UpdateLeadRequest,
    UpdateLeadResponse,
)
from .use_cases import CreateLead, DeleteLead, ReadAllLead, ReadLead, UpdateLead

router = APIRouter(prefix="/leads")


@router.post("", response_model=CreateLeadResponse)
async def create(
    request: Request,
    data: CreateLeadRequest,
    use_case: CreateLead = Depends(CreateLead),
) -> LeadSchema:
    return await use_case.execute(data.ecg_id, data.name, data.signal)


@router.get("", response_model=ReadAllLeadResponse)
async def read_all(
    request: Request,
    use_case: ReadAllLead = Depends(ReadAllLead),
) -> ReadAllLeadResponse:
    return ReadAllLeadResponse(leads=[lead async for lead in use_case.execute()])


@router.get("/{lead_id}", response_model=ReadLeadResponse)
async def read(
    request: Request,
    lead_id: int = Path(..., description=""),
    use_case: ReadLead = Depends(ReadLead),
) -> LeadSchema:
    return await use_case.execute(lead_id)


@router.put(
    "/{lead_id}",
    response_model=UpdateLeadResponse,
)
async def update(
    request: Request,
    data: UpdateLeadRequest,
    lead_id: int = Path(..., description=""),
    use_case: UpdateLead = Depends(UpdateLead),
) -> LeadSchema:
    return await use_case.execute(lead_id, data.ecg_id, data.title, data.content)


@router.delete("/{lead_id}", status_code=204)
async def delete(
    request: Request,
    lead_id: int = Path(..., description=""),
    use_case: DeleteLead = Depends(DeleteLead),
) -> None:
    await use_case.execute(lead_id)
