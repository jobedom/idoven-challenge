# pylint: disable=unused-argument

from fastapi import APIRouter, Depends, Path, Request

from ..ecg.use_cases import ReadECG
from . import calculate_insights
from .schema import ECGInsightsResponse

router = APIRouter(prefix="/insights")


@router.get("/{ecg_id}", response_model=ECGInsightsResponse)
async def read(
    request: Request,
    ecg_id: int = Path(..., description=""),
    use_case: ReadECG = Depends(ReadECG),
) -> ECGInsightsResponse:
    ecg = await use_case.execute(ecg_id)
    insights = [{"lead": lead["name"], "insights": calculate_insights(lead)} for lead in ecg.leads]
    response = {"ecg_insights": insights}
    return response
