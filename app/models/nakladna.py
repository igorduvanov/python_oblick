from sqlalchemy import VARCHAR, Column, Float, ForeignKey, Integer, String, DateTime
from app.models.base import Base
from sqlalchemy.orm import relationship
from datetime import datetime


class Nakladna(Base):
    __tablename__ = 'nakladnas'
    id = Column(Integer, primary_key=True, index=True)                      #
    number = Column(VARCHAR(13))                                            # Номер накладної
    adresa1 = Column(String)                                               # Відправник
    adresa2 = Column(String)                                               # Одержувач
    id_perelik = Column(Integer, ForeignKey("pereliks.id"))                  # 
    kilkist = Column(Float)                                                 # Кількість
    id_odvumir = Column(Integer, ForeignKey("odvumirs.id"))                 # 
    notes = Column(String)
    Perelik = relationship("Perelik")
    Odvumir = relationship("Odvumir")
    date_created = Column(DateTime(), default=datetime.utcnow)
    date_updated = Column(DateTime(), default=datetime.utcnow)
    