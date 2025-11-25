from datetime import datetime, UTC

from sqlalchemy.orm import Session

from app.adapters.db import models
from app.domain.models import RefreshToken, IRefreshToken


class RefreshTokenRepository(IRefreshToken):
    """
    Репозиторій для роботи з refresh токенами в БД.
    
    Забезпечує створення новог refresh токену та зберігає інформацію в БД.
    Автоматично трансформує моделі у доменні об'єкти.
    """
    def __init__(self, db: Session):
        self.db = db
    
    
    def create(
        self,
        user_id: int,
        token_jti: str,
        expires_at: datetime
    ) -> RefreshToken:
        """
        Створює новий refresh токен в БД.
        
        Токен автоматично помічається як не відкликаний (is_revoked=False).
        
        Args:
            user_id (int): 
            token_jti (str): 
            expires_at (datetime): 
                
        Returns:
            RefreshToken: Доменний об'єкт
        """
        token_model = models.RefreshToken(
            user_id=user_id,
            token_jti=token_jti,
            expires_at=expires_at,
            is_revoked=False
        )
        self.db.add(token_model)
        self.db.commit()
        self.db.refresh(token_model)
        
        return RefreshToken(
            id=token_model.id,
            user_id=token_model.user_id,
            token_jti=token_model.token_jti,
            is_revoked=token_model.is_revoked,
            created_at=token_model.created_at,
            expires_at=token_model.expires_at
        )