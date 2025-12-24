from dataclasses import dataclass

from fastapi import HTTPException, status
from fastapi.security import HTTPBearer
from firebase_admin import auth

security = HTTPBearer()


@dataclass
class User:
    uid: str
    email: str | None = None
    name: str | None = None
    picture: str | None = None


def verify_firebase_token(token: str) -> User:
    try:
        decoded_token = auth.verify_id_token(token)
        return User(
            uid=decoded_token["uid"],
            email=decoded_token["email"],
            name=decoded_token.get("name"),
            picture=decoded_token.get("picture"),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired Firebase token",
        ) from e
