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
    """
    Генератор для отримання SQLAlchemy сесії БД.
    
    Створює нову сесію для кожного запиту та гарантуює закриття навіть при помилках.
    
    Yields:
        Session: SQLAlchemy сесія
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearee),
    db: Session = Depends(get_db_session)
) -> User:
    """
    Отримує поточного автентифікованого користувача з JWT токена.
    
    Перевіряє JWT токен, декодує його, знаходить користувача в БД.
    Використовується як залежність для захищених ендпоінтів, які потребують аутентифікації.
    
    Args:
        credentials (HTTPAuthorizationCredentials): Bearer токен.
        db (Session): 
        
    Returns:
        User: Доменний об'єкт
    """
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