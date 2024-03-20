from fastapi import APIRouter

from .ecg.views import router as ecg_router
from .insights.views import router as insight_router
from .login.views import router as login_router
from .user.views import router as user_router

router = APIRouter()
router.include_router(login_router)
router.include_router(user_router)
router.include_router(ecg_router)
router.include_router(insight_router)
