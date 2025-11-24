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