# pylint: disable=unused-argument

from fastapi import APIRouter, Depends, HTTPException, Path, Request

from app.api.ecg.use_cases import ReadECG
from app.lib.auth import get_current_user
from app.models import User

from . import calculate_insights
from .schema import ECGInsightsResponse

router = APIRouter(prefix="/insights")


@router.get("/{ecg_id}", response_model=ECGInsightsResponse)
async def read(
    request: Request,
    ecg_id: str = Path(..., description=""),
    use_case: ReadECG = Depends(ReadECG),
    auth_user: User = Depends(get_current_user),
) -> ECGInsightsResponse:
    if auth_user.is_admin:
        raise HTTPException(status_code=403)
    ecg = await use_case.execute(ecg_id, auth_user)
    return {"ecg_insights": [{"lead": lead["name"], "insights": calculate_insights(lead)} for lead in ecg.leads]}
