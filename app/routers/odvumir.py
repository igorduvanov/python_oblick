from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from app.models.odvumir import Odvumir
from app.database import get_db
from typing import List
from pydantic import BaseModel
from datetime import datetime
from fastapi.responses import HTMLResponse
from app.templates import templates
from typing import Optional


router = APIRouter()

# Move the contents of schemas.py here
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
# End of schemas.py contents
class OdvumirOut(BaseModel):
    id: int
    name: str
    notes: str
    date_created: datetime
    date_updated: datetime

def create_odvumir_in_db(odvumir: OdvumirCreate, db: Session):
    new_odvumir = Odvumir(name=odvumir.name, notes=odvumir.notes)
    db.add(new_odvumir)
    db.commit()
    db.refresh(new_odvumir)
    return new_odvumir

# Change 'app' to 'router' in the following lines
@router.post("/odvumir/")
async def create_odvumir(odvumir: OdvumirCreate, db: Session = Depends(get_db)):
    new_odvumir = create_odvumir_in_db(odvumir, db)
    return new_odvumir

@router.get("/odvumir_page", response_class=HTMLResponse)
async def read_odvumir_page(request: Request, db: Session = Depends(get_db), search: Optional[str] = None, sort_by: Optional[str] = None):
    odvumirs = db.query(Odvumir)

    if search:
        odvumirs = odvumirs.filter(Odvumir.name.contains(search))

    if sort_by:
        if sort_by == "year_asc":
            odvumirs = odvumirs.order_by(Odvumir.date_created.asc())
        elif sort_by == "year_desc":
            odvumirs = odvumirs.order_by(Odvumir.date_created.desc())

    odvumirs = odvumirs.all()

    return templates.TemplateResponse("odvumir_page.html", {"request": request, "odvumirs": odvumirs, "search": search, "sort_by": sort_by})


@router.put("/odvumir/{odvumir_id}")
async def update_odvumir(odvumir_id: int, odvumir: OdvumirUpdate, db: Session = Depends(get_db)):
    db_odvumir = db.query(Odvumir).filter(Odvumir.id == odvumir_id).first()
    if not db_odvumir:
        raise HTTPException(status_code=404, detail="Odvumir not found")
    
    if odvumir.name is not None:
        db_odvumir.name = odvumir.name
    if odvumir.notes is not None:
        db_odvumir.notes = odvumir.notes
    
    db.commit()
    db.refresh(db_odvumir)
    return db_odvumir


@router.delete("/odvumir/{odvumir_id}")
async def delete_odvumir(odvumir_id: int, db: Session = Depends(get_db)):
    db_odvumir = db.query(Odvumir).filter(Odvumir.id == odvumir_id).first()
    if not db_odvumir:
        raise HTTPException(status_code=404, detail="Odvumir not found")
    db.delete(db_odvumir)
    db.commit()
    return {"detail": "Odvumir deleted"}
