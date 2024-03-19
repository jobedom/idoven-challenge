# pylint: disable=unused-argument

from fastapi import APIRouter, Depends, Path, Request

from app.models import ECGSchema

from .schema import (
    CreateECGRequest,
    CreateECGResponse,
    ReadAllECGResponse,
    ReadECGResponse,
    UpdateECGRequest,
    UpdateECGResponse,
)
from .use_cases import CreateECG, DeleteECG, ReadAllECG, ReadECG, UpdateECG

router = APIRouter(prefix="/ecg")


@router.post("", response_model=CreateECGResponse)
async def create(
    request: Request,
    data: CreateECGRequest,
    use_case: CreateECG = Depends(CreateECG),
) -> ECGSchema:
    return await use_case.execute(data.date)


@router.get("", response_model=ReadAllECGResponse)
async def read_all(request: Request, use_case: ReadAllECG = Depends(ReadAllECG)) -> ReadAllECGResponse:
    return ReadAllECGResponse(ecgs=[nb async for nb in use_case.execute()])


@router.get(
    "/{ecg_id}",
    response_model=ReadECGResponse,
)
async def read(
    request: Request,
    ecg_id: int = Path(..., description=""),
    use_case: ReadECG = Depends(ReadECG),
) -> ECGSchema:
    return await use_case.execute(ecg_id)


@router.put(
    "/{ecg_id}",
    response_model=UpdateECGResponse,
)
async def update(
    request: Request,
    data: UpdateECGRequest,
    ecg_id: int = Path(..., description=""),
    use_case: UpdateECG = Depends(UpdateECG),
) -> ECGSchema:
    return await use_case.execute(ecg_id, title=data.title, notes=data.notes)


@router.delete("/{ecg_id}", status_code=204)
async def delete(
    request: Request,
    ecg_id: int = Path(..., description=""),
    use_case: DeleteECG = Depends(DeleteECG),
) -> None:
    await use_case.execute(ecg_id)
