from fastapi import APIRouter

from .ecg.views import router as ecg_router
from .lead.views import router as lead_router

router = APIRouter()
router.include_router(lead_router)
router.include_router(ecg_router)
