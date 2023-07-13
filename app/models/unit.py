from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.models.base import Base

class Unit(Base):
    __tablename__ = 'units'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    notes = Column(String)
    date_created = Column(DateTime(), default=datetime.today)
    date_updated = Column(DateTime, default=datetime.today, onupdate=datetime.today)
