from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from app.database import get_db
from app.models import Robitnuk, Operation, Odvumir, Oper
from app.models.denzvit import Denzvit
from app.templates import templates
from sqlalchemy import extract

router = APIRouter()

class DenzvitBase(BaseModel):
    id_robitnuk: int
    id_operation: int
    kilkist: int
    id_odvumir: Optional[int] = None

class DenzvitCreate(DenzvitBase):
    pass

class DenzvitUpdate(DenzvitBase):
    id_robitnuk: Optional[int] = None
    id_operation: Optional[int] = None
    kilkist: Optional[int] = None
    id_odvumir: Optional[int] = None

class DenzvitInDB(DenzvitBase):
    id: int
    date_created: Optional[str] = None
    date_updated: Optional[str] = None

    class Config:
        orm_mode = True

class DenzvitOut(BaseModel):
    id: int
    id_robitnuk: int
    id_operation: int
    kilkist: int
    id_odvumir: int
    date_created: datetime
    date_updated: datetime

def create_denzvit_in_db(denzvit: DenzvitCreate, db: Session):
    new_denzvit = Denzvit(id_robitnuk=denzvit.id_robitnuk, id_operation=denzvit.id_operation,
                          kilkist=denzvit.kilkist, id_odvumir=denzvit.id_odvumir)
    db.add(new_denzvit)
    db.commit()
    db.refresh(new_denzvit)
    return new_denzvit

@router.post("/denzvit/")
async def create_denzvit(denzvit: DenzvitCreate, db: Session = Depends(get_db)):
    new_denzvit = create_denzvit_in_db(denzvit, db)
    return new_denzvit

@router.get("/denzvit_page", response_class=HTMLResponse)
async def read_denzvit_page(request: Request, db: Session = Depends(get_db), search: Optional[str] = None,
                            sort_by: Optional[str] = None, year: Optional[int] = datetime.now().year):
    denzvits = db.query(Denzvit).join(Robitnuk, Denzvit.id_robitnuk == Robitnuk.id).join(Operation, Denzvit.id_operation == Operation.id)

    robitnuks = db.query(Robitnuk).all()
    operations = db.query(Operation).join(Oper).all()
    odvumirs = db.query(Odvumir).all()

    if search:
        denzvits = denzvits.filter(Robitnuk.name.contains(search))

    if sort_by:
        if sort_by == "kilkist_asc":
            denzvits = denzvits.order_by(Denzvit.kilkist.asc())
        elif sort_by == "kilkist_desc":
            denzvits = denzvits.order_by(Denzvit.kilkist.desc())

    if year:
        denzvits = denzvits.filter(extract('year', Denzvit.date_created) == year)

    denzvits = denzvits.all()

    return templates.TemplateResponse("/templates/denzvit_page.html",
                                      {"request": request, "denzvits": denzvits, "search": search, "sort_by": sort_by, "year": year,
                                       "robitnuks": robitnuks, "operations": operations, "odvumirs": odvumirs})

@router.put("/denzvit/{denzvit_id}")
async def update_denzvit(denzvit_id: int, denzvit: DenzvitUpdate, db: Session = Depends(get_db)):
    db_denzvit = db.query(Denzvit).filter(Denzvit.id == denzvit_id).first()
    if not db_denzvit:
        raise HTTPException(status_code=404, detail="Denzvit not found")

    if denzvit.id_robitnuk is not None:
        db_denzvit.id_robitnuk = denzvit.id_robitnuk
    if denzvit.id_operation is not None:
        db_denzvit.id_operation = denzvit.id_operation
    if denzvit.kilkist is not None:
        db_denzvit.kilkist = denzvit.kilkist
    if denzvit.id_odvumir is not None:
        db_denzvit.id_odvumir = denzvit.id_odvumir

    db.commit()
    db.refresh(db_denzvit)
    return db_denzvit

@router.delete("/denzvit/{denzvit_id}")
async def delete_denzvit(denzvit_id: int, db: Session = Depends(get_db)):
    db_denzvit = db.query(Denzvit).filter(Denzvit.id == denzvit_id).first()
    if not db_denzvit:
        raise HTTPException(status_code=404, detail="Denzvit not found")
    db.delete(db_denzvit)
    db.commit()
    return {"result": "Denzvit deleted"}
