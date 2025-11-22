from typing import Optional

from sqlalchemy.orm import Session

from app.adapters.db import models
from app.domain.models import IUser, User

class UserRepository(IUser):
    def __init__(self, db: Session):
        self.db = db
    
    
    def create(
        self,
        email: str,
        password_hash: str,
        name: str
    ) -> User:
        """
        Creates user in DB.
        
        Add SQLAlchemy model, commits, updates.
        
        Return User domain object.
        """
        new_user = models.User(
            email=email,
            password_hash=password_hash,
            name=name
        )
        
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        
        return User(
            new_user.id,
            new_user.email,
            new_user.password_hash,
            new_user.name,
            new_user.created_at
        )
    
    
    def get_by_email(
        self, 
        email: str
    ) -> Optional[User]:
        """
        Searches for a user by email in the DB.
        
        Returns User domain object or None.
        """
        obj = self.db.query(models.User).filter(models.User.email == email).first()
        if obj:
            return User(obj.id, obj.email, obj.password_hash, obj.name, obj.created_at)
        return None
