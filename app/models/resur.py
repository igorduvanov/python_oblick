from sqlalchemy import Column, Float, ForeignKey, Integer, DateTime
from app.models.base import Base
from sqlalchemy.orm import relationship
from datetime import datetime


class Resur(Base):
    __tablename__ = 'resurs'
    id = Column(Integer, primary_key=True, index=True)                      #
    id_operation = Column(Integer, ForeignKey("operations.id"))             # 
    number = Column(Integer)                                               # 
    id_perelik = Column(Integer, ForeignKey("pereliks.id"))                  # 
    kilkist = Column(Float)
    id_odvumir = Column(Integer, ForeignKey("odvumirs.id"))
    Operation = relationship("Operation")
    Perelik = relationship("Perelik")
    Odvumir = relationship("Odvumir")
    date_created = Column(DateTime(), default=datetime.today)
    date_updated = Column(DateTime, default=datetime.today, onupdate=datetime.today)
