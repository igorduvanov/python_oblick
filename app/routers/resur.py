from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from app.database import get_db
from app.models import Perelik, Odvumir, Operation, Oper
from app.models.resur import Resur
from app.templates import templates
from sqlalchemy import extract

router = APIRouter()

class ResurBase(BaseModel):
    id_operation: int
    number: int
    id_perelik: int
    kilkist: float
    id_odvumir: Optional[int] = None

class ResurCreate(ResurBase):
    pass

class ResurUpdate(ResurBase):
    id_operation: Optional[int] = None
    number: Optional[int] = None
    id_perelik: Optional[int] = None
    kilkist: Optional[float] = None
    id_odvumir: Optional[int] = None

class ResurInDB(ResurBase):
    id: int
    date_created: Optional[str] = None
    date_updated: Optional[str] = None

    class Config:
        orm_mode = True

class ResurOut(BaseModel):
    id: int
    id_operation: int
    number: int
    id_perelik: int
    kilkist: float
    id_odvumir: int
    date_created: datetime
    date_updated: datetime

def create_resur_in_db(resur: ResurCreate, db: Session):
    new_resur = Resur(id_operation=resur.id_operation, number=resur.number,
                      id_perelik=resur.id_perelik, kilkist=resur.kilkist, id_odvumir=resur.id_odvumir)
    db.add(new_resur)
    db.commit()
    db.refresh(new_resur)
    return new_resur

@router.post("/resur/")
async def create_resur(resur: ResurCreate, db: Session = Depends(get_db)):
    new_resur = create_resur_in_db(resur, db)
    return new_resur

@router.get("/resur_page", response_class=HTMLResponse)
async def read_resur_page(request: Request, db: Session = Depends(get_db), search: Optional[str] = None,
                          sort_by: Optional[str] = None, year: Optional[int] = datetime.now().year):
    resurs = db.query(Resur).join(Perelik, Resur.id_perelik == Perelik.id).join(Operation, Resur.id_operation == Operation.id)

    pereliks = db.query(Perelik).all()
    operations = db.query(Operation).join(Oper).all()
    odvumirs = db.query(Odvumir).all()

    if search:
        resurs = resurs.filter(Perelik.coding.contains(search))

    if sort_by:
        if sort_by == "number_asc":
            resurs = resurs.order_by(Resur.number.asc())
        elif sort_by == "number_desc":
            resurs = resurs.order_by(Resur.number.desc())

    if year:
        resurs = resurs.filter(extract('year', Resur.date_created) == year)

    resurs = resurs.all()

    return templates.TemplateResponse("resur_page.html",
                                      {"request": request, "resurs": resurs, "search": search, "sort_by": sort_by, "year": year,
                                      "pereliks": pereliks, "operations": operations, "odvumirs": odvumirs})

@router.put("/resur/{resur_id}")
async def update_resur(resur_id: int, resur: ResurUpdate, db: Session = Depends(get_db)):
    db_resur = db.query(Resur).filter(Resur.id == resur_id).first()
    if not db_resur:
        raise HTTPException(status_code=404, detail="Resur not found")

    if resur.id_operation is not None:
        db_resur.id_operation = resur.id_operation
    if resur.number is not None:
        db_resur.number = resur.number
    if resur.id_perelik is not None:
        db_resur.id_perelik = resur.id_perelik
    if resur.kilkist is not None:
        db_resur.kilkist = resur.kilkist
    if resur.id_odvumir is not None:
        db_resur.id_odvumir = resur.id_odvumir

    db.commit()
    db.refresh(db_resur)
    return db_resur

@router.delete("/resur/{resur_id}")
async def delete_resur(resur_id: int, db: Session = Depends(get_db)):
    db_resur = db.query(Resur).filter(Resur.id == resur_id).first()
    if not db_resur:
        raise HTTPException(status_code=404, detail="Resur not found")
    db.delete(db_resur)
    db.commit()
    return {"result": "Resur deleted"}