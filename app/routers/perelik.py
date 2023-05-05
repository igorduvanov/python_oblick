from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from app.database import get_db
from app.models.perelik import Perelik
from app.templates import templates

router = APIRouter()


class PerelikBase(BaseModel):
    coding: str
    name: str
    notes: Optional[str] = None


class PerelikCreate(PerelikBase):
    pass


class PerelikUpdate(PerelikBase):
    coding: Optional[str] = None
    name: Optional[str] = None
    notes: Optional[str] = None


class PerelikInDB(PerelikBase):
    id: int
    date_created: Optional[str] = None
    date_updated: Optional[str] = None

    class Config:
        orm_mode = True

class PerelikOut(BaseModel):
    id: int
    coding: str
    name: str
    notes: str
    date_created: datetime
    date_updated: datetime


def create_perelik_in_db(perelik: PerelikCreate, db: Session):
    new_perelik = Perelik(coding=perelik.coding, name=perelik.name, notes=perelik.notes)
    db.add(new_perelik)
    db.commit()
    db.refresh(new_perelik)
    return new_perelik

@router.post("/perelik/")
async def create_perelik(perelik: PerelikCreate, db: Session = Depends(get_db)):
    new_perelik = Perelik(coding=perelik.coding, name=perelik.name, notes=perelik.notes)
    db.add(new_perelik)
    db.commit()
    db.refresh(new_perelik)
    return new_perelik


@router.get("/perelik_page", response_class=HTMLResponse)
async def read_perelik_page(request: Request, db: Session = Depends(get_db), search: Optional[str] = None,
                            sort_by: Optional[str] = None):
    pereliks = db.query(Perelik)

    if search:
        pereliks = pereliks.filter(Perelik.name.contains(search))

    if sort_by:
        if sort_by == "year_asc":
            pereliks = pereliks.order_by(Perelik.date_created.asc())
        elif sort_by == "year_desc":
            pereliks = pereliks.order_by(Perelik.date_created.desc())

    pereliks = pereliks.all()

    return templates.TemplateResponse("perelik_page.html",
                                      {"request": request, "pereliks": pereliks, "search": search, "sort_by": sort_by})


@router.put("/perelik/{perelik_id}")
async def update_perelik(perelik_id: int, perelik: PerelikUpdate, db: Session = Depends(get_db)):
    db_perelik = db.query(Perelik).filter(Perelik.id == perelik_id).first()
    if not db_perelik:
        raise HTTPException(status_code=404, detail="Perelik not found")

    if perelik.coding is not None:
        db_perelik.coding = perelik.coding
    if perelik.name is not None:
        db_perelik.name = perelik.name
    if perelik.notes is not None:
        db_perelik.notes = perelik.notes

    db.commit()
    db.refresh(db_perelik)
    return db_perelik

@router.delete("/perelik/{perelik_id}")
async def delete_perelik(perelik_id: int, db: Session = Depends(get_db)):
    db_perelik = db.query(Perelik).filter(Perelik.id == perelik_id).first()
    if not db_perelik:
        raise HTTPException(status_code=404, detail="Perelik not found")
    db.delete(db_perelik)
    db.commit()
    return {"result": "Perelik deleted"}