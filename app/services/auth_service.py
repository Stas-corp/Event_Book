from datetime import datetime, timedelta, UTC

from app.core.config import settings
from app.domain.models import IUser, IRefreshToken
from app.core.security import hash_password, verify_password, create_token_pair

class AuthService:
    """
    Сервіс для управління аутентифікацією та авторизацією користувачів.
    
    Забезпечує реєстрацію користувачів та вхід в систему.
    Використовує репозиторії для роботи з БД та функції безпеки для хешування паролів.
    """
    def __init__(
        self,
        user_repo: IUser,
        refresh_token_repo: IRefreshToken,
        jwt_secret: str,
        access_jwt_expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        refresh_jwt_expire_minutes: int = settings.REFRESH_TOKEN_EXPIRE_MINUTES
    ):
        self.user_repo = user_repo
        self.refresh_token_repo = refresh_token_repo
        self.jwt_secret = jwt_secret
        self.access_jwt_expire_minutes = access_jwt_expire_minutes
        self.refresh_jwt_expire_minutes = refresh_jwt_expire_minutes
    
    
    def register_user(
        self, 
        email: str, 
        password: str, 
        name: str
    ) -> str:
        """
        Реєструє нового користувача в системі.
        
        Перевіряє, чи email не існує, хешує пароль, створює користувача в БД,
        генерує пару JWT токенів (access + refresh) та зберігає refresh токен в БД.
        
        Args:
            email (str): 
            password (str): 
            name (str):
            
        Returns:
            dict: Словник з ключами 'access_token' та 'refresh_token'.
        """
        if self.user_repo.get_by_email(email):
            raise RuntimeError("Email already in use")
        password_hash = hash_password(password)
        user = self.user_repo.create(email, password_hash, name)
        
        tokens, refresh_payload = create_token_pair(
            user.id, 
            self.jwt_secret, 
            self.access_jwt_expire_minutes,
            self.refresh_jwt_expire_minutes
        )
        
        expires_at = datetime.now(UTC) + timedelta(minutes=self.refresh_jwt_expire_minutes)
        self.refresh_token_repo.create(
            user_id=user.id,
            token_jti=refresh_payload["jti"],
            expires_at=expires_at
        )
        
        return tokens
    
    
    def login_user(
        self,
        email: str,
        password: str
    ) -> str:
        """
        Вхід користувача в систему.
        
        Знаходить користувача за email, перевіряє пароль, та якщо вірно,
        генерує нову пару JWT токенів та зберігає refresh токен в БД.
        
        Args:
            email (str):
            password (str):
            
        Returns:
            dict: Словник з ключами 'access_token' та 'refresh_token'.
        """
        if user := self.user_repo.get_by_email(email):
            if verify_password(password, user.password_hash):
                tokens, refresh_payload = create_token_pair(
                    user.id, 
                    self.jwt_secret, 
                    self.access_jwt_expire_minutes,
                    self.refresh_jwt_expire_minutes
                )
                
                expires_at = datetime.now(UTC) + timedelta(minutes=self.refresh_jwt_expire_minutes)
                self.refresh_token_repo.create(
                    user_id=user.id,
                    token_jti=refresh_payload["jti"],
                    expires_at=expires_at
                )
                
                return tokens
            raise RuntimeError("Incorrect password")
        raise RuntimeError("Incorrect user")