from datetime import datetime

from app.domain.dtos import CreateEventDTO
from app.domain.models import IEvent, Event 


class EventService:
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
    
    
    def list_events_by_owner(
        self, 
        owner_id: int
    ) -> list[Event]:
        return self.event_repo.list_by_owner(owner_id)
