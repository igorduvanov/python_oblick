import datetime
from click import DateTime
from sqlalchemy import Column, ForeignKey, Integer
from app.models.base import Base
from sqlalchemy.orm import relationship

class Marshryt(Base):
    __tablename__ = 'marshryts'
    id = Column(Integer, primary_key=True, index=True)                      #
    id_perelik = Column(Integer, ForeignKey("pereliks.id"))                  # 
    number = Column(Integer)
    id_operation = Column(Integer, ForeignKey("operations.id"))             # 
    date_created = Column(DateTime(), default=datetime.utcnow)
    date_updated = Column(DateTime(), default=datetime.today)
    Perelik = relationship("Perelik")
    Operation = relationship("Operation")