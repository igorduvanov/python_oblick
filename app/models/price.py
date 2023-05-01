import datetime
from click import DateTime
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from app.models.base import Base
from sqlalchemy.orm import relationship


class Price(Base):
    __tablename__ = 'prices'
    id = Column(Integer, primary_key=True, index=True)                      #
    id_material = Column(Integer, ForeignKey("materials.id"))               # 
    price = Column(Float)                                                   # ціна матеріалу
    id_odvumir = Column(Integer, ForeignKey("odvumirs.id"))                 # Одиниці виміру
    notes = Column(String)                                                  #
    date_created = Column(DateTime(), default=datetime.utcnow)
    date_updated = Column(DateTime(), default=datetime.today)
    Material = relationship("Material")
    Odvumir = relationship("Odvumir")