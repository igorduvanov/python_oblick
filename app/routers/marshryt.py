from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from app.database import get_db
from app.models import Perelik, Operation, Oper
from app.models.marshryt import Marshryt
from app.templates import templates
from sqlalchemy import extract

router = APIRouter()

class MarshrytBase(BaseModel):
    id_operation: int
    number: int
    id_perelik: int

class MarshrytCreate(MarshrytBase):
    pass

class MarshrytUpdate(MarshrytBase):
    id_operation: Optional[int] = None
    number: Optional[int] = None
    id_perelik: Optional[int] = None

class MarshrytInDB(MarshrytBase):
    id: int
    date_created: Optional[str] = None
    date_updated: Optional[str] = None

    class Config:
        orm_mode = True

class MarshrytOut(BaseModel):
    id: int
    id_operation: int
    number: int
    id_perelik: int
    date_created: datetime
    date_updated: datetime

def create_marshryt_in_db(marshryt: MarshrytCreate, db: Session):
    new_marshryt = Marshryt(id_operation=marshryt.id_operation, number=marshryt.number, id_perelik=marshryt.id_perelik)
    db.add(new_marshryt)
    db.commit()
    db.refresh(new_marshryt)
    return new_marshryt

@router.post("/marshryt/")
async def create_marshryt(marshryt: MarshrytCreate, db: Session = Depends(get_db)):
    new_marshryt = create_marshryt_in_db(marshryt, db)
    return new_marshryt

@router.get("/marshryt_page", response_class=HTMLResponse)
async def read_marshryt_page(request: Request, db: Session = Depends(get_db), search: Optional[str] = None,
                          sort_by: Optional[str] = None, year: Optional[int] = datetime.now().year):
    marshryts = db.query(Marshryt).join(Perelik, Marshryt.id_perelik == Perelik.id).join(Operation, Marshryt.id_operation == Operation.id)

    pereliks = db.query(Perelik).all()
    operations = db.query(Operation).join(Oper).all()

    if search:
        marshryts = marshryts.filter(Perelik.coding.contains(search))

    if sort_by:
        if sort_by == "number_asc":
            marshryts = marshryts.order_by(Marshryt.number.asc())
        elif sort_by == "number_desc":
            marshryts = marshryts.order_by(Marshryt.number.desc())

    if year:
        marshryts = marshryts.filter(extract('year', Marshryt.date_created) == year)

    marshryts = marshryts.all()

    return templates.TemplateResponse("/templates/marshryt_page.html",
                                      {"request": request, "marshryts": marshryts, "search": search, "sort_by": sort_by, "year": year,
                                      "pereliks": pereliks, "operations": operations})

@router.put("/marshryt/{marshryt_id}")
async def update_marshryt(marshryt_id: int, marshryt: MarshrytUpdate, db: Session = Depends(get_db)):
    db_marshryt = db.query(Marshryt).filter(Marshryt.id == marshryt_id).first()
    if not db_marshryt:
        raise HTTPException(status_code=404, detail="Marshryt not found")

    if marshryt.id_operation is not None:
        db_marshryt.id_operation = marshryt.id_operation
    if marshryt.number is not None:
        db_marshryt.number = marshryt.number
    if marshryt.id_perelik is not None:
        db_marshryt.id_perelik = marshryt.id_perelik

    db.commit()
    db.refresh(db_marshryt)
    return db_marshryt

@router.delete("/marshryt/{marshryt_id}")
async def delete_marshryt(marshryt_id: int, db: Session = Depends(get_db)):
    db_marshryt = db.query(Marshryt).filter(Marshryt.id == marshryt_id).first()
    if not db_marshryt:
        raise HTTPException(status_code=404, detail="Marshryt not found")
    db.delete(db_marshryt)
    db.commit()
    return {"result": "Marshryt deleted"}
