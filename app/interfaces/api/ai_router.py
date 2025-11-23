from fastapi import APIRouter

from app.interfaces.api import API_V1

router = APIRouter(prefix=f"{API_V1}/ai", tags=["AI"])
