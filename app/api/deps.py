import jwt
from sqlalchemy.orm import Session
from fastapi import HTTPException, Request, Depends

from app.core.config import settings
from app.adapters.db.base import SessionLocal
from app.core.security import decode_jwt_token
from app.adapters.repo.user import UserRepository, User

def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    request: Request,
    db: Session = Depends(get_db_session)
    ) -> User:
    auth_header = request.headers.get("Authorization")
    
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Missing or invalid authorization header",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    token = auth_header.split(" ")[1]
    
    try:
        payload = decode_jwt_token(
            token,
            settings.JWT_SECRET_KEY,
            token_type="access"
        )
        
        user_repo = UserRepository(db)
        user = user_repo.get_by_id(payload["user_id"])
        
        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        
        return user
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Access token expired",
            headers={"WWW-Authenticate": "Bearer"}
        )
        
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )