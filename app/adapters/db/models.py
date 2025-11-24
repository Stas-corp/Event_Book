from datetime import datetime, UTC

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    Integer, 
    String, 
    DateTime, 
    ForeignKey, 
    Text,
    Boolean
)

from app.adapters.db.base import Base


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(UTC))
    
    events: Mapped['Event'] = relationship("Event", back_populates="owner")
    bookings: Mapped['Booking'] = relationship("Booking", back_populates="user")
    refresh_tokens: Mapped['RefreshToken'] = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")


class Event(Base):
    __tablename__ = "events"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text)
    datetime: Mapped['datetime'] = mapped_column(DateTime, nullable=False)
    max_seats: Mapped[int] = mapped_column(Integer, nullable=False)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    
    owner: Mapped['User'] = relationship("User", back_populates="events")
    bookings: Mapped['Booking'] = relationship("Booking", back_populates="event")


class Booking(Base):
    __tablename__ = "bookings"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int]= mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey("events.id"), nullable=False)
    seats_booked: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(UTC))
    
    user: Mapped['User']  = relationship("User", back_populates="bookings")
    event: Mapped['Event'] = relationship("Event", back_populates="bookings")


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    token_jti: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(UTC))
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    
    user: Mapped['User']  = relationship("User", back_populates="refresh_tokens")