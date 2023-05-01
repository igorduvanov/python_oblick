import datetime
from click import DateTime
from sqlalchemy import Column, Integer, String
from app.models.base import Base


class Robitnuk(Base):
    __tablename__ = 'robitnuks'
    id = Column(Integer, primary_key=True, index=True)                      #
    name = Column(String)                                                   # Ім'я
    notes = Column(String)                                                  #
    date_created = Column(DateTime(), default=datetime.utcnow)
    date_updated = Column(DateTime(), default=datetime.today)