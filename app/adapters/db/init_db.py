from sqlalchemy import inspect
from app.adapters.db.base import Base, engine
from app.adapters.db.models import User, Event, Booking
import logging

logger = logging.getLogger(__name__)

def init_db():
    """
    Checks for the tables in the database.
    
    If the tables do not exist - creates them.
    """
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    
    expected_tables = {"users", "events", "bookings", "refresh_tokens"}
    
    if not existing_tables:
        Base.metadata.create_all(bind=engine)
    elif expected_tables - set(existing_tables):
        Base.metadata.create_all(bind=engine)
