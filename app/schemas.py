from pydantic import BaseModel
from typing import Optional

class OdvumirBase(BaseModel):
    name: str
    notes: Optional[str] = None

class OdvumirCreate(OdvumirBase):
    pass

class OdvumirUpdate(OdvumirBase):
    name: Optional[str] = None
    notes: Optional[str] = None

class OdvumirInDB(OdvumirBase):
    id: int
    date_created: Optional[str] = None
    date_updated: Optional[str] = None

    class Config:
        orm_mode = True
