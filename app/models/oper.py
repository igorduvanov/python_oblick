from sqlalchemy import Column, Integer, String, DateTime
from app.models.base import Base
from datetime import datetime

class Oper(Base):
    __tablename__ = 'opers'
    id = Column(Integer, primary_key=True, index=True)                      #
    name = Column(String)                                                   # операції по стандарту
    cod = Column(String)                                                    #
    date_created = Column(DateTime(), default=datetime.utcnow)
    date_updated = Column(DateTime(), default=datetime.today)