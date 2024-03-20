# pylint: disable=unused-argument

from fastapi import APIRouter, Depends, HTTPException, Path, Request

from app.lib.auth import get_current_user
from app.models import ECGSchema, User

from .schema import CreateECGRequest, CreateECGResponse, ReadECGResponse
from .use_cases import CreateECG, DeleteECG, ReadECG

router = APIRouter(prefix="/ecg")


@router.post("", response_model=CreateECGResponse)
async def create(
    request: Request,
    data: CreateECGRequest,
    use_case: CreateECG = Depends(CreateECG),
    auth_user: User = Depends(get_current_user),
) -> ECGSchema:
    for lead in data.leads:
        signal_length = len(lead["signal"])
        if lead.get("sample_count"):
            if lead["sample_count"] != signal_length:
                raise HTTPException(status_code=422)  # 422 Unprocessable Entity
        else:
            lead["sample_count"] = signal_length
    return await use_case.execute(data.id, data.date, data.leads, auth_user)


@router.get("/{ecg_id}", response_model=ReadECGResponse)
async def read(
    request: Request,
    ecg_id: str = Path(..., description=""),
    use_case: ReadECG = Depends(ReadECG),
    auth_user: User = Depends(get_current_user),
) -> ECGSchema:
    return await use_case.execute(ecg_id, auth_user)


@router.delete("/{ecg_id}", status_code=204)
async def delete(
    request: Request,
    ecg_id: str = Path(..., description=""),
    use_case: DeleteECG = Depends(DeleteECG),
    auth_user: User = Depends(get_current_user),
) -> None:
    await use_case.execute(ecg_id, auth_user)
