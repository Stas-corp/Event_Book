from datetime import datetime, UTC

from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column, 
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
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(UTC))
    
    events = relationship("Event", back_populates="owner")
    bookings = relationship("Booking", back_populates="user")
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")


class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    datetime = Column(DateTime, nullable=False)
    max_seats = Column(Integer, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    owner = relationship("User", back_populates="events")
    bookings = relationship("Booking", back_populates="event")


class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    seats_booked = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now(UTC))
    
    user = relationship("User", back_populates="bookings")
    event = relationship("Event", back_populates="bookings")


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token_jti = Column(String, unique=True, index=True, nullable=False)
    is_revoked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now(UTC))
    expires_at = Column(DateTime, nullable=False)
    
    user = relationship("User", back_populates="refresh_tokens")