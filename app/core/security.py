import uuid
from typing import Literal

import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, UTC

from app.core.config import settings

pwd_context = CryptContext(
    schemes=["argon2", "bcrypt"], 
    deprecated="auto"
    )


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_jwt_token(
    user_id: int, 
    secret: str, 
    expires_minutes: int,
    token_type: Literal["access", "refresh"] = "access"
) -> tuple[str, dict]:
    expire = datetime.now(UTC) + timedelta(minutes=expires_minutes)
    jti = str(uuid.uuid4())
    
    payload = {
        "user_id": user_id, 
        "exp": expire,
        "type": token_type,
        "jti": jti,
        "iat": datetime.now(UTC)
    }
    
    return jwt.encode(payload, secret, algorithm="HS256"), payload


def decode_jwt_token(
    token: str, 
    secret: str,
    token_type: Literal["access", "refresh"] = "access"
) -> dict:
    payload = jwt.decode(token, secret, algorithms=["HS256"])
    if payload.get("type") != token_type:
        raise jwt.InvalidTokenError(f"Expected {token_type} token")
    
    return payload


def create_token_pair(
    user_id: int,
    secret: str,
    access_expires_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    refresh_expires_minutes: int = settings.REFRESH_TOKEN_EXPIRE_MINUTES
) -> tuple[dict, dict]:
    """
    Creates a pair of tokens, access and refresh.
    
    Returns:
        tuple: A tuple containing two dict:
        - First dict:
            - access_token (str): JWT access token.
            - refresh_token (str): JWT refresh token.
        - Second dict:
            - refresh_payload (dict): payload refresh token.
    
    Example:
        >>> tokens, payload = create_token_pair("user123")
        >>> print(tokens["access_token"])
        
    """
    access_token, _ = create_jwt_token(
        user_id=user_id,
        secret=secret,
        expires_minutes=access_expires_minutes,
        token_type="access"
    )
    
    refresh_token, refresh_payload = create_jwt_token(
        user_id=user_id,
        secret=secret,
        expires_minutes=refresh_expires_minutes,
        token_type="refresh"
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }, refresh_payload


def refresh_access_token(
    refresh_token: str,
    secret: str,
    access_expires_minutes: int = 15
) -> str:
    payload = decode_jwt_token(refresh_token, secret, token_type="refresh")
    
    new_access_token = create_jwt_token(
        user_id=payload["user_id"],
        secret=secret,
        expires_minutes=access_expires_minutes,
        token_type="access"
    )
    
    return new_access_token