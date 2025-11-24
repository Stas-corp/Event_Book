from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Security

from app.domain.models import User
from app.domain.dtos import CreateEventDTO
from app.services.event_service import EventService
from app.adapters.repo.event_repo import EventRepository
from app.api.deps import get_db_session, get_current_user

router = APIRouter()


class EventResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    datetime: datetime
    max_seats: int
    owner_id: int


class EventCreate(BaseModel):
    title: str
    description: Optional[str]
    datetime: datetime
    max_seats: int


@router.post("/event")
def my_events(
    body: EventCreate,
    db: Session = Depends(get_db_session),
    user: User = Security(get_current_user)
):
    event_repo = EventRepository(db)
    service = EventService(event_repo)
    event_dto = CreateEventDTO(**body.model_dump(), owner_id=user.id)
    return service.create_event(event_dto)


@router.get("/my/events", response_model=List[EventResponse])
def my_events(
    db: Session = Depends(get_db_session),
    user: User = Security(get_current_user)
):
    event_repo = EventRepository(db)
    service = EventService(event_repo)
    return [EventResponse(**vars(e)) for e in service.list_events_by_owner(user.id)]