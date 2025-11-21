import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, UTC

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
    expires_minutes: int
) -> str:
    expire = datetime.now(UTC) + timedelta(minutes=expires_minutes)
    payload = {"user_id": user_id, "exp": expire}
    return jwt.encode(payload, secret, algorithm="HS256")

def decode_jwt_token(
    token: str, 
    secret: str
) -> dict:
    return jwt.decode(token, secret, algorithms=["HS256"])