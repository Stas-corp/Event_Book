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


@router.post("/register")
def register_user(
    payload: RegisterRequest,
    db: Session = Depends(get_db_session)
):
    user_repo = UserRepository(db)
    service = AuthService(
        user_repo, 
        settings.JWT_SECRET_KEY, 
        settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        settings.REFRESH_TOKEN_EXPIRE_MINUTES
    )
    try:
        token = service.register_user(
            payload.email, 
            payload.password, 
            payload.name
        )
        return {
            "tokens": token,
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
