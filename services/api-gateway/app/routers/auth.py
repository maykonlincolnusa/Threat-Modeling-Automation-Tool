from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..security import UserClaims, authenticate_user, create_access_token

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/token")
def issue_token(payload: LoginRequest):
    user = authenticate_user(payload.username, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user)
    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role,
    }


@router.get("/roles")
def list_roles():
    return {
        "roles": [
            {"name": "viewer", "permissions": ["read:overview"]},
            {"name": "analyst", "permissions": ["read:overview", "create:threat_event"]},
            {"name": "admin", "permissions": ["*"]},
        ]
    }
