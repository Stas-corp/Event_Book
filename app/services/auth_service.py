from app.domain.models import IUser
from app.core.config import settings
from app.core.security import hash_password, verify_password, create_token_pair

class AuthService:
    def __init__(
        self,
        user_repo: IUser,
        jwt_secret: str,
        access_jwt_expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        refresh_jwt_expire_minutes: int = settings.REFRESH_TOKEN_EXPIRE_MINUTES
    ):
        self.user_repo = user_repo
        self.jwt_secret = jwt_secret
        self.access_jwt_expire_minutes = access_jwt_expire_minutes
        self.refresh_jwt_expire_minutes = refresh_jwt_expire_minutes
    
    
    def register_user(
        self, 
        email: str, 
        password: str, 
        name: str
    ) -> str:
        if self.user_repo.get_by_email(email):
            raise RuntimeError("Email already in use")
        password_hash = hash_password(password)
        user = self.user_repo.create(email, password_hash, name)
        
        return create_token_pair(
            user.id, 
            self.jwt_secret, 
            self.access_jwt_expire_minutes,
            self.refresh_jwt_expire_minutes
        )
    
    
    def login_user(
        self,
        email: str,
        password: str
    ) -> str:
        if user := self.user_repo.get_by_email(email):
            if verify_password(password, user.password_hash):
                return create_token_pair(
                    user.id, 
                    self.jwt_secret, 
                    self.access_jwt_expire_minutes,
                    self.refresh_jwt_expire_minutes
                )
            raise RuntimeError("Incorrect password")
        raise RuntimeError("Incorrect user")