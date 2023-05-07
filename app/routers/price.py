from app.models.material import Material
from app.models.odvumir import Odvumir
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from app.database import get_db
from app.models.price import Price
from app.templates import templates


router = APIRouter()

# Move the contents of schemas.py here
class PriceBase(BaseModel):
    id_material: int
    price: float
    id_odvumir: int
    notes: Optional[str] = None

class PriceCreate(PriceBase):
    pass

class PriceUpdate(PriceBase):
    id_material: Optional[int] = None
    price: Optional[float] = None
    id_odvumir: Optional[int] = None
    notes: Optional[str] = None

class PriceInDB(PriceBase):
    id: int
    date_created: Optional[str] = None
    date_updated: Optional[str] = None

    class Config:
        orm_mode = True

# End of schemas.py contents
class PriceOut(BaseModel):
    id: int
    id_material: int
    price: float
    id_odvumir: int
    notes: Optional[str]
    date_created: datetime
    date_updated: datetime

def create_price_in_db(price: PriceCreate, db: Session):
    new_price = Price(id_material=price.id_material, price=price.price, id_odvumir=price.id_odvumir, notes=price.notes)
    db.add(new_price)
    db.commit()
    db.refresh(new_price)
    return new_price

@router.post("/price/")
async def create_price(price: PriceCreate, db: Session = Depends(get_db)):
    new_price = create_price_in_db(price, db)
    return new_price


@router.get("/price_page", response_class=HTMLResponse)
async def read_price_page(request: Request, db: Session = Depends(get_db), search: Optional[str] = None,
                            sort_by: Optional[str] = None):
    prices = db.query(Price)  

    materials = db.query(Material).all()
    odvumirs = db.query(Odvumir).all()  

    if search:
        prices = prices.filter(Price.notes.contains(search))

    if sort_by:
        if sort_by == "year_asc":
            prices = prices.order_by(Price.date_created.asc())
        elif sort_by == "year_desc":
            prices = prices.order_by(Price.date_created.desc())

    prices = prices.all()

    return templates.TemplateResponse("price_page.html",
                                      {"request": request, "prices": prices, "search": search, "sort_by": sort_by,
                                       "materials": materials, "odvumirs": odvumirs})

@router.put("/price/{price_id}")
async def update_price(price_id: int, price: PriceUpdate, db: Session = Depends(get_db)):
    db_price = db.query(Price).filter(Price.id == price_id).first()
    if not db_price:
        raise HTTPException(status_code=404, detail="Price not found")

    if price.id_material is not None:
        db_price.id_material = price.id_material
    if price.price is not None:
        db_price.price = price.price
    if price.id_odvumir is not None:
        db_price.id_odvumir = price.id_odvumir
    if price.notes is not None:
        db_price.notes = price.notes

    db.commit()
    db.refresh(db_price)
    return db_price

@router.delete("/price/{price_id}")
async def delete_price(price_id: int, db: Session = Depends(get_db)):
    db_price = db.query(Price).filter(Price.id ==price_id).first()
    if not db_price:
        raise HTTPException(status_code=404, detail="Price not found")
    db.delete(db_price)
    db.commit()
    return {"detail": "price deleted"}
