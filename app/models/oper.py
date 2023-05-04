import datetime
from click import DateTime
from sqlalchemy import Column, Integer, String
from app.models.base import Base


class Oper(Base):
    __tablename__ = 'opers'
    id = Column(Integer, primary_key=True, index=True)                      #
    name = Column(String)                                                   # операції по стандарту
    cod = Column(String)                                                    #
    date_created = Column(DateTime(), default=datetime.utcnow)
    date_updated = Column(DateTime(), default=datetime.today)