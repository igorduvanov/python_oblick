from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.models.base import Base

class Odvumir(Base):
    __tablename__ = 'odvumirs'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    notes = Column(String)
    date_created = Column(DateTime(), default=datetime.utcnow)
    date_updated = Column(DateTime(), default=datetime.today)