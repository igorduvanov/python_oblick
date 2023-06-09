from app.models.odvumir import Odvumir
from app.models.unit import Unit
from app.models.perelik import Perelik
from app.models.nakladna import Nakladna
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from app.database import get_db
from app.templates import templates

router = APIRouter()

class NakladnaBase(BaseModel):
    number: str
    address_1: int  # Changed id_unit to address_1
    address_2: int  # Added address_2
    id_perelik: int
    kilkist: float
    id_odvumir: int
    notes: Optional[str] = None

class NakladnaCreate(NakladnaBase):
    pass

class NakladnaUpdate(NakladnaBase):
    number: Optional[str] = None
    address_1: Optional[int] = None  # Changed id_unit to address_1
    address_2: Optional[int] = None  # Added address_2
    id_perelik: Optional[int] = None
    kilkist: Optional[float] = None
    id_odvumir: Optional[int] = None
    notes: Optional[str] = None

class NakladnaInDB(NakladnaBase):
    id: int
    date_created: Optional[str] = None
    date_updated: Optional[str] = None

    class Config:
        orm_mode = True

class NakladnaOut(NakladnaInDB):
    pass

def create_nakladna_in_db(nakladna: NakladnaCreate, db: Session):
    new_nakladna = Nakladna(number=nakladna.number, address_1=nakladna.address_1, address_2=nakladna.address_2,
                            id_perelik=nakladna.id_perelik, kilkist=nakladna.kilkist, 
                            id_odvumir=nakladna.id_odvumir, notes=nakladna.notes)
    db.add(new_nakladna)
    db.commit()
    db.refresh(new_nakladna)
    return new_nakladna

@router.post("/nakladna/")
async def create_nakladna(nakladna: NakladnaCreate, db: Session = Depends(get_db)):
    new_nakladna = create_nakladna_in_db(nakladna, db)
    return new_nakladna

@router.get("/nakladna_page", response_class=HTMLResponse)
async def read_nakladna_page(request: Request, db: Session = Depends(get_db), search: Optional[str] = None,
                              sort_by: Optional[str] = None):
    nakladnas = db.query(Nakladna)

    units = db.query(Unit).all()
    pereliks = db.query(Perelik).all()
    odvumirs = db.query(Odvumir).all()

    if search:
        nakladnas = nakladnas.filter(Nakladna.number.contains(search))

    if sort_by:
        if sort_by == "year_asc":
            nakladnas = nakladnas.order_by(Nakladna.date_created.asc())
        elif sort_by == "year_desc":
            nakladnas = nakladnas.order_by(Nakladna.date_created.desc())

    nakladnas = nakladnas.all()

    # Create a dictionary mapping unit ids to unit names
    unit_names = {unit.id: unit.name for unit in units}

    return templates.TemplateResponse("/templates/nakladna_page.html",
            {"request":request, "nakladnas": nakladnas, "search": search, "sort_by": sort_by,
            "units": units, "unit_names": unit_names, "pereliks": pereliks,"odvumirs": odvumirs})

@router.put("/nakladna/{nakladna_id}")
async def update_nakladna(nakladna_id: int, nakladna: NakladnaUpdate, db: Session = Depends(get_db)):
    db_nakladna = db.query(Nakladna).filter(Nakladna.id == nakladna_id).first()
    if not db_nakladna:
        raise HTTPException(status_code=404, detail="Nakladna not found")
    if nakladna.number is not None:
        db_nakladna.number = nakladna.number
    if nakladna.address_1 is not None:
        db_nakladna.address_1 = nakladna.address_1
    if nakladna.address_2 is not None:
        db_nakladna.address_2 = nakladna.address_2
    if nakladna.id_perelik is not None:
        db_nakladna.id_perelik = nakladna.id_perelik
    if nakladna.kilkist is not None:
        db_nakladna.kilkist = nakladna.kilkist
    if nakladna.id_odvumir is not None:
        db_nakladna.id_odvumir = nakladna.id_odvumir
    if nakladna.notes is not None:
        db_nakladna.notes = nakladna.notes

    db.commit()
    db.refresh(db_nakladna)
    return db_nakladna

@router.delete("/nakladna/{nakladna_id}")
async def delete_nakladna(nakladna_id: int, db: Session = Depends(get_db)):
    db_nakladna = db.query(Nakladna).filter(Nakladna.id == nakladna_id).first()
    if not db_nakladna:
        raise HTTPException(status_code=404, detail="Nakladna not found")
    db.delete(db_nakladna)
    db.commit()
    return {"detail": "nakladna deleted"}    