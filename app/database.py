from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .config import settings
from contextlib import contextmanager

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

