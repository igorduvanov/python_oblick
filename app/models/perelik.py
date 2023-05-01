import datetime
from click import DateTime
from sqlalchemy import Column, Integer, String
from app.models.base import Base

class Perelik(Base):                                                       # Перелік деталей, матеріалів ...
    __tablename__ = 'pereliks'
    id = Column(Integer, primary_key=True, index=True)                      #
    coding = Column(String)                                                 # Кодування
    name = Column(String)                                                   # Марка матеріалу
    notes = Column(String)                                                  # Приміітки
    date_created = Column(DateTime(), default=datetime.utcnow)
    date_updated = Column(DateTime(), default=datetime.today)