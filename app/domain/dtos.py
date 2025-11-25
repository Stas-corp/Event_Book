from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class CreateEventDTO(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=5000)
    datetime: datetime
    max_seats: int = Field(..., gt=0, le=10000)
    owner_id: int = Field(..., gt=0)


class CreateBookingDTO(BaseModel):
    user_id: int = Field(..., gt=0)
    event_id: int = Field(..., gt=0)
    seats_booked: int = Field(..., gt=0)