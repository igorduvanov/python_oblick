from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from app.models.robitnuk import Robitnuk
from app.database import get_db
from typing import List
from pydantic import BaseModel
from datetime import datetime
from fastapi.responses import HTMLResponse
from app.templates import templates
from typing import Optional


router = APIRouter()

# Move the contents of schemas.py here
class RobitnukBase(BaseModel):
    name: str
    notes: Optional[str] = None

class RobitnukCreate(RobitnukBase):
    pass

class RobitnukUpdate(RobitnukBase):
    name: Optional[str] = None
    notes: Optional[str] = None

class RobitnukInDB(RobitnukBase):
    id: int
    date_created: Optional[str] = None
    date_updated: Optional[str] = None

    class Config:
        orm_mode = True
# End of schemas.py contents
class RobitnukOut(BaseModel):
    id: int
    name: str
    notes: str
    date_created: datetime
    date_updated: datetime

def create_robitnuk_in_db(robitnuk: RobitnukBase, db: Session):
    new_robitnuk = Robitnuk(name=robitnuk.name, notes=robitnuk.notes)
    db.add(new_robitnuk)
    db.commit()
    db.refresh(new_robitnuk)
    return new_robitnuk

# Change 'app' to 'router' in the following lines
@router.post("/robitnuk/")
async def create_odvumir(robitnuk: RobitnukCreate, db: Session = Depends(get_db)):
    new_robitnuk = create_robitnuk_in_db(robitnuk, db)
    return new_robitnuk

@router.get("/robitnuk_page", response_class=HTMLResponse)
async def read_robitnuk_page(request: Request, db: Session = Depends(get_db), search: Optional[str] = None, sort_by: Optional[str] = None):
    robitnuk = db.query(Robitnuk)

    if search:
        robitnuk = robitnuk.filter(Robitnuk.name.contains(search))

    if sort_by:
        if sort_by == "year_asc":
            robitnuk = robitnuk.order_by(Robitnuk.date_created.asc())
        elif sort_by == "year_desc":
            robitnuk = robitnuk.order_by(Robitnuk.date_created.desc())

    robitnuk = robitnuk.all()

    return templates.TemplateResponse("robitnuk_page.html", {"request": request, "robitnuk": robitnuk, "search": search, "sort_by": sort_by})


@router.put("/robitnuk/{robitnuk_id}")
async def update_robitnuk(robitnuk_id: int, robitnuk: RobitnukUpdate, db: Session = Depends(get_db)):
    db_robitnuk = db.query(Robitnuk).filter(Robitnuk.id == robitnuk_id).first()
    if not db_robitnuk:
        raise HTTPException(status_code=404, detail="Robitnuk not found")
    
    if robitnuk.name is not None:
        db_robitnuk.name = robitnuk.name
    if robitnuk.notes is not None:
        db_robitnuk.notes = robitnuk.notes
    
    db.commit()
    db.refresh(db_robitnuk)
    return db_robitnuk


@router.delete("/robitnuk/{robitnuk_id}")
async def delete_robitnuk(robitnuk_id: int, db: Session = Depends(get_db)):
    db_robitnuk = db.query(Robitnuk).filter(Robitnuk.id == robitnuk_id).first()
    if not db_robitnuk:
        raise HTTPException(status_code=404, detail="Robitnuk not found")
    db.delete(db_robitnuk)
    db.commit()
    return {"detail": "Robitnuk deleted"}
