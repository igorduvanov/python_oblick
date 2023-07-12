from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.models.base import Base

class Robitnuk(Base):
    __tablename__ = 'robitnuks'
    id = Column(Integer, primary_key=True, index=True)                      #
    name = Column(String)                                                   # Ім'я
    notes = Column(String)                                                  #
    date_created = Column(DateTime(), default=datetime.today)
    date_updated = Column(DateTime, default=datetime.today, onupdate=datetime.today)
