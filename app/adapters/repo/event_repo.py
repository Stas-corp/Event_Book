from sqlalchemy.orm import Session

from app.adapters.db import models
from app.domain.dtos import CreateEventDTO
from app.domain.models import Event, IEvent, Booking


class EventRepository(IEvent):
    def __init__(self, db: Session):
        self.db = db
    
    
    def create(
        self,
        dto: CreateEventDTO
    ) -> Event:
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
        if obj:
            return obj
        return None
    
    
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
        if obj:
            return obj
        return None
    
    
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