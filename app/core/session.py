import os
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt

from app.core.security import User

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
SESSION_EXPIRE_DAYS = 1


def create_session_token(user: User) -> str:
    expire = datetime.utcnow() + timedelta(days=SESSION_EXPIRE_DAYS)
    to_encode = {
        "uid": user.uid,
        "email": user.email,
        "name": user.name,
        "picture": user.picture,
        "exp": expire,
    }

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_session_token(token: str) -> Optional[User]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = User(
            uid=payload.get("uid"),
            email=payload.get("email"),
            name=payload.get("name"),
            picture=payload.get("picture"),
        )
        return user
    except JWTError:
        return None
