from sqlalchemy.orm import Session

from app.adapters.db import models
from app.domain.dtos import CreateBookingDTO
from app.domain.models import Booking, Event, IBooking


class BookingRepository(IBooking):
    def __init__(self, db: Session):
        self.db = db
    
    
    def create(
        self,
        dto: CreateBookingDTO
    ) -> Booking:
        new_book = models.Booking(**dto.__dict__)
        
        self.db.add(new_book)
        self.db.commit()
        self.db.refresh(new_book)
        
        return self._map_to_domain(new_book)
    
    
    def list_by_user(
        self,
        user_id: int
    ) -> list[tuple[Event, Booking]]:
        booking_obj = self.db.query(models.Booking).filter(models.Booking.user_id == user_id).all()
        if booking_obj:
            result = [(booking.event, booking) for booking in booking_obj]
            return result
        return None
    
    
    def _map_to_domain(
        self, 
        db_event: models.Booking
    ) -> Booking:
        return Booking(
            id=db_event.id,
            user_id=db_event.user_id,
            event_id=db_event.event_id,
            seats_booked=db_event.seats_booked,
            created_at=db_event.created_at,
        )