from sqlalchemy import Column, ForeignKey, Integer, DateTime #Sequence
from sqlalchemy.sql import func
from app.models.base import Base
from sqlalchemy.orm import relationship

class Operation(Base):
    __tablename__ = 'operations'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True) 
    #id = Column(Integer, Sequence('operation_id_seq'), primary_key=True, index=True)  або або так
    id_perelik = Column(Integer, ForeignKey("pereliks.id"))
    id_oper = Column(Integer, ForeignKey("opers.id"))
    Perelik = relationship("Perelik")
    Oper = relationship("Oper")
    date_created = Column(DateTime, server_default=func.now()) 
    date_updated = Column(DateTime, server_default=func.now(), onupdate=func.now()) 
