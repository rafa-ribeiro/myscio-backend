from typing import Optional

from pydantic import BaseModel


class LoginRequest(BaseModel):
    id_token: str


class UserResponse(BaseModel):
    uid: str
    email: Optional[str] = None
    name: Optional[str] = None
    picture: Optional[str] = None


class AuthResponse(BaseModel):
    success: bool
    message: str
    user: Optional[UserResponse] = None
