from datetime import datetime

from app.domain.models import IEvent, Event 


class EventService:
    def __init__(
        self,
        event_repo: IEvent,
    ):
        self.event_repo = event_repo
    
    
    def create_event(
        self, 
        title: str, 
        description: str, 
        datetime_: datetime, 
        max_seats: int, 
        owner_id: int
    ) -> Event:
        return self.event_repo.create(
            title, 
            description, 
            datetime_, 
            max_seats, 
            owner_id
        )
    
    
    def list_events_by_owner(
        self, 
        owner_id: int
    ) -> list[Event]:
        return self.event_repo.list_by_owner(owner_id)
