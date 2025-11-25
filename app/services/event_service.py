from datetime import datetime

from app.domain.dtos import CreateEventDTO
from app.domain.models import IEvent, Event 


class EventService:
    """
    Сервіс для управління подіями та їх операціями.
    
    Забезпечує створення нових подій, пошук подій за ID, отримання бронювань
    для конкретної подієї та отримання всіх подій, створених конкретним користувачем.
    Використовує репозиторій для роботи з БД.
    """
    def __init__(
        self,
        event_repo: IEvent,
    ):
        self.event_repo = event_repo
    
    
    def create_event(
        self,
        event_dto: CreateEventDTO
    ) -> Event:
        return self.event_repo.create(
            event_dto
        )
    
    
    def event_by_id(
        self,
        event_id: int
    ) -> Event:
        return self.event_repo.event_by_event_id(event_id)
    
    
    def books_by_id(
        self,
        event_id: int
    ) -> Event:
        return self.event_repo.books_by_event_id(event_id)
    
    
    def list_events_by_owner(
        self, 
        owner_id: int
    ) -> list[Event]:
        return self.event_repo.list_by_owner(owner_id)
