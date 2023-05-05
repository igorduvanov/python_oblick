import datetime
from click import DateTime
from sqlalchemy import Column, ForeignKey, Integer
from app.models.base import Base
from sqlalchemy.orm import relationship


class Operation(Base):
    __tablename__ = 'operations'
    id = Column(Integer, primary_key=True, index=True)                      #
    id_perelik = Column(Integer, ForeignKey("pereliks.id"))                 # 
    id_oper = Column(Integer, ForeignKey("opers.id"))                       # 
    Perelik = relationship("Perelik")
    Oper = relationship("Oper")
    date_created = Column(DateTime(), default=datetime.utcnow)
    date_updated = Column(DateTime(), default=datetime.today)