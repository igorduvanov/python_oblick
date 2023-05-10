from sqlalchemy import Column, Float, Integer, String, DateTime, ForeignKey
from app.models.base import Base
from datetime import datetime
from sqlalchemy.orm import relationship


class Material(Base):
    __tablename__ = 'materials'
    id = Column(Integer, primary_key=True, index=True)  
    id_perelik = Column(Integer, ForeignKey("pereliks.id"))               # 
    weight= Column(Float)         
    id_odvumir = Column(Integer, ForeignKey("odvumirs.id"))                 #
    notes = Column(String)                            
    Perelik = relationship("Perelik") 
    Odvumir = relationship("Odvumir")                     #
    date_created = Column(DateTime(), default=datetime.utcnow)
    date_updated = Column(DateTime(), default=datetime.today)