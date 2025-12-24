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


@router.get("/protected")
def protected_route(user=Depends(verify_session_token)):
    return {
        "message": "Você está autenticado",
        "uid": user.uid,
        "email": user.email,
    }
