import os
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

security = HTTPBearer(auto_error=True)

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-this-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "90"))


class UserClaims(BaseModel):
    sub: str
    role: str


DEMO_USERS = {
    "viewer": {"password": "viewer123", "role": "viewer"},
    "analyst": {"password": "analyst123", "role": "analyst"},
    "admin": {"password": "admin123", "role": "admin"},
}


def authenticate_user(username: str, password: str) -> UserClaims | None:
    data = DEMO_USERS.get(username)
    if not data or data["password"] != password:
        return None
    return UserClaims(sub=username, role=data["role"])


def create_access_token(claims: UserClaims) -> str:
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=JWT_EXPIRE_MINUTES)
    payload = {
        "sub": claims.sub,
        "role": claims.role,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserClaims:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return UserClaims(sub=payload["sub"], role=payload["role"])
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired token: {exc}",
        ) from exc


def require_roles(allowed_roles: list[str]):
    def _role_check(user: UserClaims = Depends(get_current_user)) -> UserClaims:
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{user.role}' is not allowed",
            )
        return user

    return _role_check
