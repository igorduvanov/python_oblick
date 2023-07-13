from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.models.base import Base

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)                      #
    login = Column(String)                                                  #Ім'я
    password = Column(String) 
    role = Column(String)                                                   # 
    notes = Column(String)                                                  #
    date_created = Column(DateTime(), default=datetime.today)
    date_updated = Column(DateTime, default=datetime.today, onupdate=datetime.today)
