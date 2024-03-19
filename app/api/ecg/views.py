# pylint: disable=unused-argument

from fastapi import APIRouter, Depends, HTTPException, Path, Request

from app.models import ECGSchema

from .schema import CreateECGRequest, CreateECGResponse, ReadAllECGResponse, ReadECGResponse
from .use_cases import CreateECG, DeleteECG, ReadAllECG, ReadECG

router = APIRouter(prefix="/ecg")


@router.post("", response_model=CreateECGResponse)
async def create(
    request: Request,
    data: CreateECGRequest,
    use_case: CreateECG = Depends(CreateECG),
) -> ECGSchema:
    for lead in data.leads:
        signal_length = len(lead["signal"])
        if lead.get("sample_count"):
            if lead["sample_count"] != signal_length:
                raise HTTPException(status_code=422)  # 422 Unprocessable Entity
        else:
            lead["sample_count"] = signal_length
    return await use_case.execute(data.date, data.leads)


@router.get("", response_model=ReadAllECGResponse)
async def read_all(
    request: Request,
    use_case: ReadAllECG = Depends(ReadAllECG),
) -> ReadAllECGResponse:
    return ReadAllECGResponse(ecgs=[ecg async for ecg in use_case.execute()])


@router.get("/{ecg_id}", response_model=ReadECGResponse)
async def read(
    request: Request,
    ecg_id: int = Path(..., description=""),
    use_case: ReadECG = Depends(ReadECG),
) -> ECGSchema:
    return await use_case.execute(ecg_id)


@router.delete("/{ecg_id}", status_code=204)
async def delete(
    request: Request,
    ecg_id: int = Path(..., description=""),
    use_case: DeleteECG = Depends(DeleteECG),
) -> None:
    await use_case.execute(ecg_id)
