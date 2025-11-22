from typing import Annotated

from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, StringConstraints
from fastapi import APIRouter, Depends, HTTPException

from app.core.config import settings
from app.api.deps import get_db_session
from app.adapters.repo.user import UserRepository
from app.services.auth_service import AuthService

router = APIRouter()

PasswordStr = Annotated[str, StringConstraints(min_length=6)]
NameStr = Annotated[str, StringConstraints(min_length=1)]


class RegisterRequest(BaseModel):
    email: EmailStr
    password: PasswordStr
    name: NameStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: PasswordStr


@router.post("/register")
def register_user(
    payload: RegisterRequest,
    db: Session = Depends(get_db_session)
):
    user_repo = UserRepository(db)
    service = AuthService(
        user_repo, 
        settings.JWT_SECRET_KEY
    )
    try:
        tokens = service.register_user(
            payload.email, 
            payload.password, 
            payload.name
        )
        
        return {
            "tokens": tokens,
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def Login_user(
    payload: LoginRequest,
    db: Session = Depends(get_db_session)
):
    user_repo = UserRepository(db)
    service = AuthService(
        user_repo, 
        settings.JWT_SECRET_KEY
    )
    
    try:
        tokens = service.login_user(
            payload.email,
            payload.password
        )
        
        return {
            "tokens": tokens,
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))