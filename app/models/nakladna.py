from sqlalchemy import VARCHAR, Column, Float, ForeignKey, Integer, String, DateTime
from app.models.base import Base
from sqlalchemy.orm import relationship
from datetime import datetime


class Nakladna(Base):
    __tablename__ = 'nakladnas'
    id = Column(Integer, primary_key=True, index=True)
    number = Column(VARCHAR(13))      
    address_1 = Column(Integer, ForeignKey("units.id"))  # Replaced id_unit with address_1
    address_2 = Column(Integer, ForeignKey("units.id"))  # Added address_2
    id_perelik = Column(Integer, ForeignKey("pereliks.id"))
    kilkist = Column(VARCHAR(13))                                                 
    id_odvumir = Column(Integer, ForeignKey("odvumirs.id"))
    notes = Column(VARCHAR(13))
    Unit1 = relationship("Unit", foreign_keys=[address_1])  # Renamed relationship to Unit1
    Unit2 = relationship("Unit", foreign_keys=[address_2])  # Added relationship for address_2
    Perelik = relationship("Perelik")
    Odvumir = relationship("Odvumir")
    date_created = Column(DateTime(), default=datetime.utcnow)
    date_updated = Column(DateTime(), default=datetime.utcnow)
