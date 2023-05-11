from sqlalchemy import VARCHAR, Column, Float, ForeignKey, Integer, String, DateTime
from app.models.base import Base
from sqlalchemy.orm import relationship
from datetime import datetime


class Nakladna(Base):
    __tablename__ = 'nakladnas'
    id = Column(Integer, primary_key=True, index=True)                      #
    number = Column(VARCHAR(13))      
    id_unit = Column(Integer, ForeignKey("units.id"))                  #                                      # Номер накладної                                          # Одержувач
    id_perelik = Column(Integer, ForeignKey("pereliks.id"))                  # 
    kilkist = Column(Float)                                                 # Кількість
    id_odvumir = Column(Integer, ForeignKey("odvumirs.id"))                 # 
    notes = Column(String)
    Unit = relationship("Unit")
    Perelik = relationship("Perelik")
    Odvumir = relationship("Odvumir")
    date_created = Column(DateTime(), default=datetime.utcnow)
    date_updated = Column(DateTime(), default=datetime.utcnow)
    