from app.domain.models import IUser
from app.core.security import hash_password, create_jwt_token

class AuthService:
    def __init__(self, user_repo: IUser, jwt_secret: str, jwt_expire_minutes: int):
        self.user_repo = user_repo
        self.jwt_secret = jwt_secret
        self.jwt_expire_minutes = jwt_expire_minutes

    def register_user(self, email: str, password: str, name: str) -> str:
        if self.user_repo.get_by_email(email):
            raise RuntimeError("Email already in use")
        password_hash = hash_password(password)
        user = self.user_repo.create(email, password_hash, name)
        return create_jwt_token(user.id, self.jwt_secret, self.jwt_expire_minutes)