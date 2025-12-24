from fastapi import APIRouter, status, Depends
from pydantic import BaseModel

from app.core.session import verify_session_token


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


@router.get(
    path="/protected",
    responses={status.HTTP_200_OK: {"description": "Protected route access - Only for authenticated users"}},
    response_model=dict
)
def protected_route(user=Depends(verify_session_token)) -> dict:
    return {
        "message": "You are authenticated",
        "uid": user.uid,
        "email": user.email,
    }
