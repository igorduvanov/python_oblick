import datetime
from click import DateTime
from sqlalchemy import VARCHAR, Column, Float, ForeignKey, Integer, String
from app.models.base import Base
from sqlalchemy.orm import relationship


class Nakladna(Base):
    __tablename__ = 'nakladnas'
    id = Column(Integer, primary_key=True, index=True)                      #
    number = Column(VARCHAR(13))                                            # Номер накладної
    adresa1 = Column(Integer)                                               # Відправник
    adresa2 = Column(Integer)                                               # Одержувач
    id_perelik = Column(Integer, ForeignKey("pereliks.id"))                  # 
    kilkist = Column(Float)                                                 # Кількість
    id_odvumir = Column(Integer, ForeignKey("odvumirs.id"))                 # 
    notes = Column(String)
    date_created = Column(DateTime(), default=datetime.utcnow)
    date_updated = Column(DateTime(), default=datetime.utcnow)
    Perelik = relationship("Perelik")
    Odvumir = relationship("Odvumir")