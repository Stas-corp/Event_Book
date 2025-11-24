from datetime import datetime
from typing import Optional, Protocol

# Domain entitiens

class User:
    def __init__(
        self,
        id: int,
        name: str,
        email: str,
        password_hash: str,
        created_at: datetime
    ):
        self.id = id
        self.name = name
        self.email = email
        self.created_at = created_at
        self.password_hash = password_hash


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
        self.created_at = created_at
        self.seats_booked = seats_booked


class RefreshToken:
    def __init__(
        self,
        id: int,
        user_id: int,
        token_jti: str,
        is_revoked: bool,
        created_at: datetime,
        expires_at: datetime
    ):
        self.id = id
        self.user_id = user_id
        self.token_jti = token_jti
        self.is_revoked = is_revoked
        self.created_at = created_at
        self.expires_at = expires_at


# Repository interfaces

class IUser(Protocol):
    def create(
        self, 
        email: str, 
        password_hash: str, 
        name: str
    ) -> User: ...
    
    
    def get_by_email(
        self,
        email: str
    ) -> Optional[User]: ...
    
    
    def get_by_id(
        self,
        id: int
    ) -> Optional[User]: ...


class IEvent(Protocol):
    def create(
        self, 
        title: str, 
        description: str, 
        datetime: datetime, 
        max_seats: int, 
        owner_id: int
    ) -> Event: ...
    
    
    def list_by_owner(
        owner_id: int
    ) -> Optional[list[Event]]: ...


class IBooking(Protocol):
    def create(
        self,
        user_id: int,
        event_id: int,
        seats_booked: int
    ) -> Booking: ...


class IRefreshToken(Protocol):
    def create(
        self,
        user_id: int,
        token_jti: str,
        expires_at: datetime
    ) -> RefreshToken: ...
    
    
    def get_by_jti(
        self,
        token_jti: str
    ) -> Optional[RefreshToken]: ...
    
    
    def is_valid(
        self,
        token_jti: str
    ) -> bool: ...
    
    
    def revoke(
        self,
        token_jti: str
    ) -> None: ...
