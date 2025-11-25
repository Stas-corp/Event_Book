from sqlalchemy.orm import Session

from app.adapters.db import models
from app.domain.dtos import CreateEventDTO
from app.domain.models import Event, IEvent, Booking


class EventRepository(IEvent):
    """
    Репозиторій для роботи з подіями в БД.
    
    Керує CRUD операціями для подій, створення нових подій,
    пошук подій, отримання всіх подій конкретного власника,
    та отримання всіх бронювань для конкретної подієї.
    Автоматично трансформує моделі у доменні об'єкти.
    
    Attributes:
        db (Session): SQLAlchemy сесія
    """
    def __init__(self, db: Session):
        self.db = db
    
    
    def create(
        self,
        dto: CreateEventDTO
    ) -> Event:
        """
        Створює нову подію в БД.
        
        Приймає DTO з даними події, створює новий запис в таблиці events,
        комітить зміни та повертає доменний об'єкт.
        
        Args:
            dto (CreateEventDTO): 
            
        Returns:
            Event: Доменний об'єкт
            
        """
        new_event = models.Event(**dto.__dict__)
        
        self.db.add(new_event)
        self.db.commit()
        self.db.refresh(new_event)
        
        return self._map_to_domain(new_event)
    
    
    def list_by_owner(
        self,
        owner_id: int
    ) -> list[Event]:
        obj = self.db.query(models.Event).filter(models.Event.owner_id == owner_id).all()
        return [self._map_to_domain(o) for o in obj]
    
    
    def event_by_event_id(
        self, 
        event_id: int
    ) -> Event:
        obj = self.db.query(models.Event).filter(models.Event.id == event_id).first()
        if obj:
            return self._map_to_domain(obj)
        return None
    
    
    def books_by_event_id(
        self,
        event_id: int
    ) -> list[Booking]:
        obj = self.db.query(models.Booking).filter(models.Booking.event_id == event_id).all()
        return [self._map_to_domain(o) for o in obj]
    
    
    def _map_to_domain(
        self, 
        db_event: models.Event
    ) -> Event:
        return Event(
            id=db_event.id,
            title=db_event.title,
            description=db_event.description,
            datetime=db_event.datetime,
            max_seats=db_event.max_seats,
            owner_id=db_event.owner_id
        )