from fastapi import APIRouter, HTTPException
from app.core.auth import LoginRequest, authenticate_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(data: LoginRequest):
    user = authenticate_user(data.user_id)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "access_token": str(user["id"]),
        "token_type": "bearer"
    }