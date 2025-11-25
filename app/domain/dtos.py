from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class CreateEventDTO:
    title: str
    description: Optional[str]
    datetime: datetime
    max_seats: int
    owner_id: int


@dataclass
class CreateBookingDTO:
    user_id: int
    event_id: int
    seats_booked: int