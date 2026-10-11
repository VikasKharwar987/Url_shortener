from fastapi import APIRouter, HTTPException, Depends
from app.models.user_model import (UserCreate, UserLogin, create_user, get_user_by_email, get_user_by_id)
from app.utils.password import verify_password
from app.utils.jwt_handler import create_access_token
from app.utils.auth import get_current_user

router = APIRouter()


@router.get("/api/auth/me")
def get_my_profile(
    user_id: int = Depends(get_current_user)
):
    result = get_user_by_id(user_id)
    if result is None:
        raise HTTPException(
            status_code=401,
            detail="User no longer exists"
        )
    return {
        "id": result[0],
        "username": result[1],
        "email": result[2]
    }


@router.post("/api/auth/registry")
def register_user(user: UserCreate):
    result = create_user(
        user.username,
        user.email,
        user.password
    )
    return {
        "message": "User registered successfully",
        "user": {
            "id": result[0],
            "username": result[1],
            "email": result[2],
            "created_at": result[3]
        }
    }

@router.post("/api/auth/login")
def login_user(user: UserLogin):
    result = get_user_by_email(user.email)
    if result is None:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    password_hash = result[3]
    if not verify_password(user.password, password_hash):
        raise HTTPException(status_code = 401, detail="Invalid email or password")
    access_token = create_access_token(result[0])
    return{
        "message": "login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": result[0],
            "username": result[1],
            "email": result[2]
        }
    }