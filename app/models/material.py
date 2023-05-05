from sqlalchemy import Column, Float, Integer, String, DateTime
from app.models.base import Base
from datetime import datetime


class Material(Base):
    __tablename__ = 'materials'
    id = Column(Integer, primary_key=True, index=True)                      #
    profile = Column(String)                                                # Профіль
    marka = Column(String)                                                  # Марка матеріалу
    weight= Column(Float)                                                   # Вага п/м
    notes = Column(String)                                                  #
    date_created = Column(DateTime(), default=datetime.utcnow)
    date_updated = Column(DateTime(), default=datetime.today)