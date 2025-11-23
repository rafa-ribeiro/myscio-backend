from fastapi import APIRouter

from app.interfaces.api.documents_router import router as documents_router
from app.interfaces.api.health_router import router as health_router

router = APIRouter()
router.include_router(health_router)
router.include_router(documents_router)
