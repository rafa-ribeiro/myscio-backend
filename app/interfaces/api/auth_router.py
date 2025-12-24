import logging
from typing import Optional

from dependency_injector.wiring import inject
from fastapi import APIRouter, status, Response, Cookie, HTTPException

from app.core.security import verify_firebase_token
from app.core.session import create_session_token, verify_session_token
from app.interfaces.api import API_V1
from app.interfaces.api.auth_schemas import AuthResponse, LoginRequest, UserResponse

router = APIRouter(prefix=f"{API_V1}/auth", tags=["Auth"])
logger = logging.getLogger(__name__)

SESSION_TOKEN_KEY = "session_token"


@router.post(
    path="/login",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"description": "Successful login"}},
    response_model=AuthResponse
)
@inject
async def login(login_data: LoginRequest, response: Response):
    user = verify_firebase_token(token=login_data.id_token)

    session_token = create_session_token(user=user)

    response.set_cookie(
        key=SESSION_TOKEN_KEY,
        value=session_token,
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="lax",
        max_age=3600 * 24  # 1 day
    )

    logger.info(f"User {user.email} logged in successfully.")

    return AuthResponse(
        success=True,
        message="Login successful",
        user=UserResponse(
            uid=user.uid,
            email=user.email,
            name=user.name,
            picture=user.picture
        )
    )


@router.get(
    path="/verify",
    status_code=status.HTTP_200_OK,
    response_model=AuthResponse
)
async def verify(session_token: Optional[str] = Cookie(None)):
    if not session_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No session token provided")

    try:
        user = verify_session_token(token=session_token)

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired session token")

        return AuthResponse(
            success=True,
            message="Session is valid",
            user=UserResponse(
                uid=user.uid,
                email=user.email,
                name=user.name,
                picture=user.picture
            )
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error verifying session token: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.post(
    path="/logout",
    status_code=status.HTTP_200_OK,
)
async def logout(response: Response):
    try:
        response.delete_cookie(
            key=SESSION_TOKEN_KEY,
            path="/",
            samesite="lax"
        )

        logger.info("Logout successful - cookie deleted")

        return {
            "success": True,
            "message": "Logout successful"
        }
    except Exception as e:
        logger.error(f"Error during logout: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
