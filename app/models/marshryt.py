from sqlalchemy import Column, ForeignKey, Integer, DateTime
from app.models.base import Base
from sqlalchemy.orm import relationship
from datetime import datetime


class Marshryt(Base):
    __tablename__ = 'marshryts'
    id = Column(Integer, primary_key=True, index=True)                      #
    id_perelik = Column(Integer, ForeignKey("pereliks.id"))                  # 
    number = Column(Integer)
    id_operation = Column(Integer, ForeignKey("operations.id"))     
    
    Perelik = relationship("Perelik")
    Operation = relationship("Operation")
    date_created = Column(DateTime, default=datetime.today)
    date_updated = Column(DateTime, default=datetime.today, onupdate=datetime.today)

   