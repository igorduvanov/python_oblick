from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from app.database import get_db
from app.models.oper import Oper
from app.templates import templates

router = APIRouter()


# Move the contents of schemas.py here
class OperBase(BaseModel):
    name: str
    cod: Optional[str] = None


class OperCreate(OperBase):
    pass


class OperUpdate(OperBase):
    name: Optional[str] = None
    cod: Optional[str] = None


class OperInDB(OperBase):
    id: int
    date_created: Optional[str] = None
    date_updated: Optional[str] = None

    class Config:
        orm_mode = True


# End of schemas.py contents
class OperOut(BaseModel):
    id: int
    name: str
    cod: str
    date_created: datetime
    date_updated: datetime


def create_oper_in_db(oper: OperCreate, db: Session):
    new_oper = Oper(name=oper.name, cod=oper.cod)
    db.add(new_oper)
    db.commit()
    db.refresh(new_oper)
    return new_oper


# Change 'app' to 'router' in the following lines
@router.post("/oper/")
async def create_oper(oper: OperCreate, db: Session = Depends(get_db)):
    new_oper = create_oper_in_db(oper, db)
    return new_oper


@router.get("/oper_page", response_class=HTMLResponse)
async def read_oper_page(request: Request, db: Session = Depends(get_db), search: Optional[str] = None,
                            sort_by: Optional[str] = None):
    oper = db.query(Oper)

    if search:
        oper = oper.filter(Oper.name.contains(search))

    if sort_by:
        if sort_by == "year_asc":
            oper = oper.order_by(Oper.date_created.asc())
        elif sort_by == "year_desc":
            oper = oper.order_by(Oper.date_created.desc())

    oper = oper.all()

    return templates.TemplateResponse("oper_page.html",
                                      {"request": request, "oper": oper, "search": search, "sort_by": sort_by})


@router.put("/oper/{oper_id}")
async def update_oper(oper_id: int, oper: OperUpdate, db: Session = Depends(get_db)):
    db_oper = db.query(Oper).filter(Oper.id == oper_id).first()
    if not db_oper:
        raise HTTPException(status_code=404, detail="Oper not found")

    if oper.name is not None:
        db_oper.name = oper.name
    if oper.cod is not None:
        db_oper.cod = oper.cod

    db.commit()
    db.refresh(db_oper)
    return db_oper


@router.delete("/oper/{oper_id}")
async def delete_oper(oper_id: int, db: Session = Depends(get_db)):
    db_oper = db.query(Oper).filter(Oper.id == oper_id).first()
    if not db_oper:
        raise HTTPException(status_code=404, detail="Oper not found")
    db.delete(db_oper)
    db.commit()
    return {"detail": "oper deleted"}