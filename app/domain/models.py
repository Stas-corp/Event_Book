from datetime import datetime
from typing import Optional, Protocol, List

# Domain entitiens

class User:
    def __init__(
        self,
        id: int,
        email: str,
        password_hash: str,
        name: str,
        created_at: datetime
    ):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.name = name
        self.created_at = created_at

class Event:
    def __init__(
        self,
        id: int,
        title: str,
        description: Optional[str],
        datetime: datetime,
        max_seats: int,
        owner_id: int
    ):
        self.id = id
        self.title = title
        self.description = description
        self.datetime = datetime
        self.max_seats = max_seats
        self.owner_id = owner_id

class Booking:
    def __init__(
        self,
        id: int,
        user_id: int,
        event_id: int,
        seats_booked: int,
        created_at: datetime
    ):
        self.id = id
        self.user_id = user_id
        self.event_id = event_id
        self.seats_booked = seats_booked
        self.created_at = created_at

# Repository interfaces

class IUser(Protocol):
    def create(
        self, 
        email: str, 
        password_hash: str, 
        name: str
    ) -> User: ...

class IEvent(Protocol):
    def create(
        self, 
        title: str, 
        description: str, 
        datetime: datetime, 
        max_seats: int, 
        owner_id: int
    ) -> Event: ...

class IBooking(Protocol):
    def create(
        self,
        user_id: int,
        event_id: int,
        seats_booked: int
    ) -> Booking: ...
