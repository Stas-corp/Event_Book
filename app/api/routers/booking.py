from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, Security, Path

from app.domain.models import User
from app.domain.dtos import CreateBookingDTO
from app.services.booking_service import BookingService
from app.adapters.repo.event_repo import EventRepository
from app.adapters.repo.booking_repo import BookingRepository
from app.api.deps import get_db_session, get_current_user

router = APIRouter()


class BookingCreate(BaseModel):
    seats_booked: int = Field(..., gt=0)


@router.post("/events/{id}/book")
def book_event(
    body: BookingCreate,
    id: int = Path(..., description="Id event"),
    db: Session = Depends(get_db_session),
    user: User = Security(get_current_user)
):
    booking_repo = BookingRepository(db)
    event_repo = EventRepository(db)
    service = BookingService(
        booking_repo,
        event_repo
    )
    
    event_dto = CreateBookingDTO(
        event_id=id,
        user_id=user.id,
        seats_booked=body.seats_booked
    )
    
    return service.create_book_event(event_dto)



@router.get("/my/booking")
def my_events(
    db: Session = Depends(get_db_session),
    user: User = Security(get_current_user)
):
    booking_repo = BookingRepository(db)
    event_repo = EventRepository(db)
    service = BookingService(
        booking_repo,
        event_repo)
    return service.list_book_events(
        user_id=user.id
    )