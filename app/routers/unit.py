from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from app.models.unit import Unit
from app.database import get_db
from typing import List
from pydantic import BaseModel
from datetime import datetime
from fastapi.responses import HTMLResponse
from app.templates import templates
from typing import Optional


router = APIRouter()

# Move the contents of schemas.py here
class UnitBase(BaseModel):
    name: str
    notes: Optional[str] = None

class UnitCreate(UnitBase):
    pass

class UnitUpdate(UnitBase):
    name: Optional[str] = None
    notes: Optional[str] = None

class UnitInDB(UnitBase):
    id: int
    date_created: Optional[str] = None
    date_updated: Optional[str] = None

    class Config:
        orm_mode = True
# End of schemas.py contents
class UnitOut(BaseModel):
    id: int
    name: str
    notes: str
    date_created: datetime
    date_updated: datetime

def create_unit_in_db(unit: UnitCreate, db: Session):
    new_unit = Unit(name=unit.name, notes=unit.notes)
    db.add(new_unit)
    db.commit()
    db.refresh(new_unit)
    return new_unit

@router.post("/unit/")
async def create_unit(unit: UnitCreate, db: Session = Depends(get_db)):
    new_unit = create_unit_in_db(unit, db)
    return new_unit

@router.get("/unit_page", response_class=HTMLResponse)
async def read_unit_page(request: Request, db: Session = Depends(get_db), search: Optional[str] = None, sort_by: Optional[str] = None):
    units = db.query(Unit)

    if search:
        units = units.filter(Unit.name.contains(search))

    if sort_by:
        if sort_by == "year_asc":
            units = units.order_by(Unit.date_created.asc())
        elif sort_by == "year_desc":
            units = units.order_by(Unit.date_created.desc())

    units = units.all()

    return templates.TemplateResponse("unit_page.html", {"request": request, "units": units, "search": search, "sort_by": sort_by})

@router.put("/unit/{unit_id}")
async def update_unit(unit_id: int, unit: UnitUpdate, db: Session = Depends(get_db)):
    db_unit = db.query(Unit).filter(Unit.id == unit_id).first()
    if not db_unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    
    if unit.name is not None:
        db_unit.name = unit.name
    if unit.notes is not None:
        db_unit.notes = unit.notes
    
    db.commit()
    db.refresh(db_unit)
    return db_unit

@router.delete("/unit/{unit_id}")
async def delete_unit(unit_id: int, db: Session = Depends(get_db)):
    db_unit = db.query(Unit).filter(Unit.id == unit_id).first()
    if not db_unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    db.delete(db_unit)
    db.commit()
    return {"detail": "Unit deleted"}
