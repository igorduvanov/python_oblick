from sqlalchemy.orm import Session
from app.models.base import engine, SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
