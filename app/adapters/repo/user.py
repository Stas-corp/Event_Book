from typing import Optional

from sqlalchemy.orm import Session

from app.adapters.db import models
from app.domain.models import IUser, User

class UserRepository(IUser):
    """
    Репозиторій для роботи з користувачами в БД.
    
    Забезпечує операції CRUD для користувачів, включаючи пошук за email та ID.
    Трансформує DB моделі у доменні об'єкти.
    
    Attributes:
        db (Session): SQLAlchemy сесія для роботи з БД.
    """
    def __init__(self, db: Session):
        self.db = db
    
    
    def create(
        self,
        email: str,
        password_hash: str,
        name: str
    ) -> User:
        """
        Створює нового користувача в БД.
        
        Додає новий запис користувача, фіксує зміни в БД,
        оновлює об'єкт та повертає доменний об'єкт User.
        
        Args:
            email (str): Унікальна email адреса користувача.
            password_hash (str): Захешована пароль користувача.
            name (str): Ім'я користувача.
            
        Returns:
            User: Доменний об'єкт
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
        Пошук користувача за email адресою.
        
        Виконує запит до БД для знаходження користувача з заданним email.
        
        Args:
            email (str):
            
        Returns:
            Optional[User]: Доменний об'єкт
        """
        obj: User = self.db.query(models.User).filter(models.User.email == email).first()
        if obj:
            return User(
                id=obj.id, 
                email=obj.email, 
                password_hash=obj.password_hash, 
                name=obj.name, 
                created_at=obj.created_at
            )
        return None
    
    
    def get_by_id(
        self, 
        id: int
    ) -> Optional[User]:
        """
        Пошук користувача за його ID.
        
        Виконує запит до БД для знаходження користувача з заданим ID.
        
        Args:
            id (int):
            
        Returns:
            Optional[User]: Доменний об'єкт
        """
        obj: User = self.db.query(models.User).filter(models.User.id == id).first()
        if obj:
            return User(
                id=obj.id, 
                email=obj.email, 
                password_hash=obj.password_hash, 
                name=obj.name, 
                created_at=obj.created_at
            )
        return None
