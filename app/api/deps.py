from app.adapters.db.base import SessionLocal

def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()