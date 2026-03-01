from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class LoginRequest(BaseModel):
    user_id: int


def authenticate_user(user_id: int):
    if user_id == 1:
        return {"id": 1, "username": "student1"}
    elif user_id == 2:
        return {"id": 2, "username": "student2"}
    else:
        return None


def get_current_user(token: str = Depends(oauth2_scheme)):

    try:
        user_id = int(token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    user = authenticate_user(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user