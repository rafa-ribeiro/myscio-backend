from fastapi import APIRouter, status
from pydantic import BaseModel


class HealthResponse(BaseModel):
    message: str


router = APIRouter(prefix="/health", tags=["health-check"])


@router.get(
    path="/",
    responses={status.HTTP_200_OK: {"description": "Health response OK"}},
    response_model=HealthResponse,
)
async def health():
    return HealthResponse(message="It's running!")
