from fastapi import HTTPException, status

from app.domain.dtos import CreateBookingDTO
from app.domain.models import  Booking, Event, IBooking, IEvent


class BookingService:
    """
    Сервіс для управління бронюванням подій.
    
    Забезпечує створення бронювань та отримання списку заброньованих подій
    користувачем.
    Перевіряє доступність місць та першкоджає повторного дублювання одним користувачем.
    """
    def __init__(
        self,
        booking_repo: IBooking,
        event_repo: IEvent
    ):
        self.booking_repo = booking_repo
        self.event_repo = event_repo
    
    
    def create_book_event(
        self,
        booking_dto: CreateBookingDTO
    ) -> Booking:
        """
        Створює бронювання користувача на подію.
        
        Перевіряє:
        - Чи існує подія
        - Чи користувач не заброньував цю подію раніше
        - Чи достатньо вільних місць для запиту
        
        Якщо всі перевірки пройдено, створює бронювання в БД.
        
        Args:
            booking_dto (CreateBookingDTO):
            
        Returns:
            Booking: Доменний об'єкт.
            
        """
        event = self.event_repo.event_by_event_id(booking_dto.event_id)
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The event does not exist"
            )
        
        users_event_book = self.list_book_events(booking_dto.user_id)
        
        if users_event_book:
            for event_booked, _ in users_event_book:
                if event_booked.id == booking_dto.event_id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="The event has already been booked by you"
                    )
        
        total_booked = self.event_repo.books_by_event_id(booking_dto.event_id)
        if total_booked: 
            total_seats_booked = sum([book.seats_booked for book in total_booked])
        else: 
            total_seats_booked = 0
        if not event.has_available_seats(
            total_seats_booked, 
            booking_dto.seats_booked
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No availabil requested seats"
            )
        
        return self.booking_repo.create(
            booking_dto
        )
    
    
    def list_book_events(
        self, 
        user_id: int
    ) -> list[tuple[Event, Booking]]:
        return self.booking_repo.list_by_user(user_id)
