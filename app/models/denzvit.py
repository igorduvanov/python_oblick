import datetime
from click import DateTime
from sqlalchemy import Column, ForeignKey, Integer
from app.models.base import Base
from sqlalchemy.orm import relationship

class Denzvit(Base):
    __tablename__ = 'denzvits'
    id = Column(Integer, primary_key=True, index=True)                      #
    id_robitnuk = Column(Integer, ForeignKey("robitnuks.id"))               # 
    id_operation = Column(Integer, ForeignKey("operations.id"))             # 
    kilkist = Column(Integer)
    id_odvumir = Column(Integer, ForeignKey("odvumirs.id"))                 # 
    date_created = Column(DateTime(), default=datetime.utcnow)
    date_updated = Column(DateTime(), default=datetime.today)
    Robitnuk = relationship("Robitnuk")
    Operation = relationship("Operation")
    Odvumir = relationship("Odvumir")