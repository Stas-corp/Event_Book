from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
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
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=5000)
    datetime: datetime
    max_seats: int = Field(..., gt=0)


@router.post("/event")
def create_event(
    body: EventCreate,
    db: Session = Depends(get_db_session),
    user: User = Security(get_current_user)
):
    event_repo = EventRepository(db)
    service = EventService(event_repo)
    event_dto = CreateEventDTO(**body.model_dump(), owner_id=user.id)
    return service.create_event(event_dto)


@router.get("/my/events")
def get_my_events(
    db: Session = Depends(get_db_session),
    user: User = Security(get_current_user)
):
    event_repo = EventRepository(db)
    service = EventService(event_repo)
    events = service.list_events_by_owner(user.id)
    if events:
        return [EventResponse(**vars(e)) for e in events]
    return None