import os
import logging
import importlib

from sqlalchemy import inspect

import app.core.config as config_mod
import app.adapters.db.base as base_mod


# Set DATABASE_URL to in-memory
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

# Reload config and base 
importlib.reload(config_mod)
importlib.reload(base_mod)

import app.adapters.db.models

def test_create_tables_using_project_engine():
    """Use the `engine` (recreated with test DATABASE_URL) 
    to create tables and assert `users` exists."""
    engine = base_mod.engine
    Base = base_mod.Base
    
    try:
        Base.metadata.create_all(engine)
        
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        assert "users" in tables
        assert "bookings" in tables
        assert "events" in tables
        
        logging.info(f"Tables successfully created!")
        
    finally:
        try:
            engine.dispose()
        except Exception:
            pass
