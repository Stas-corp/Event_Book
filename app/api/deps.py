import jwt
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.config import settings
from app.adapters.db.base import SessionLocal
from app.core.security import decode_jwt_token
from app.adapters.repo.user import UserRepository
from app.domain.models import User

http_bearee = HTTPBearer()

def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearee),
    db: Session = Depends(get_db_session)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        payload = decode_jwt_token(
            token,
            settings.JWT_SECRET_KEY,
            token_type="access"
        )
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
            
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    except jwt.InvalidTokenError:
        raise credentials_exception

    user_repo = UserRepository(db)
    user = user_repo.get_by_id(user_id)
    
    if user is None:
        raise credentials_exception
    
    return user