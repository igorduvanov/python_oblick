from sqlalchemy import Column, Integer, String, DateTime
from app.models.base import Base
from datetime import datetime

class Perelik(Base):                                                       # Перелік деталей, матеріалів ...
    __tablename__ = 'pereliks'
    id = Column(Integer, primary_key=True, index=True)                      #
    coding = Column(String)                                                 # Кодування
    name = Column(String)                                                   # Марка матеріалу
    notes = Column(String)                                                  # Приміітки
    date_created = Column(DateTime, default=datetime.today)
    date_updated = Column(DateTime, default=datetime.today, onupdate=datetime.today)
