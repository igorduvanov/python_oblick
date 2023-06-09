from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from app.database import get_db
from app.models import Perelik, Odvumir
from app.models.material import Material
from app.templates import templates
from sqlalchemy import extract

router = APIRouter()

class MaterialBase(BaseModel):
    weight: float
    notes: Optional[str] = None
    id_perelik: Optional[int] = None
    id_odvumir: Optional[int] = None

class MaterialCreate(MaterialBase):
    pass

class MaterialUpdate(MaterialBase):
    weight: Optional[float] = None
    notes: Optional[str] = None
    id_perelik: Optional[int] = None
    id_odvumir: Optional[int] = None

class MaterialInDB(MaterialBase):
    id: int
    date_created: Optional[str] = None
    date_updated: Optional[str] = None

    class Config:
        orm_mode = True

class MaterialOut(BaseModel):
    id: int
    weight: float
    notes: str
    date_created: datetime
    date_updated: datetime

def create_material_in_db(material: MaterialCreate, db: Session):
    new_material = Material(weight=material.weight, notes=material.notes,
                            id_perelik=material.id_perelik, id_odvumir=material.id_odvumir)
    db.add(new_material)
    db.commit()
    db.refresh(new_material)
    return new_material

@router.post("/material/")
async def create_material(material: MaterialCreate, db: Session = Depends(get_db)):
    new_material = create_material_in_db(material, db)
    return new_material

@router.get("/material_page", response_class=HTMLResponse)
async def read_material_page(request: Request, db: Session = Depends(get_db), search: Optional[str] = None,
                             sort_by: Optional[str] = None, year: Optional[int] = datetime.now().year):
    materials = db.query(Material).join(Perelik, Material.id_perelik == Perelik.id)

    pereliks = db.query(Perelik).all()
    odvumirs = db.query(Odvumir).all()

    if search:
        materials = materials.filter(Perelik.coding.contains(search))

    if sort_by:
        if sort_by == "weight_asc":
            materials = materials.order_by(Material.weight.asc())
        elif sort_by == "weight_desc":
            materials = materials.order_by(Material.weight.desc())

    if year:
        materials = materials.filter(extract('year', Material.date_created) == year)

    materials = materials.all()

    return templates.TemplateResponse("/templates/material_page.html",
                                      {"request": request, "materials": materials, "search": search, "sort_by": sort_by, "year": year,
                                       "pereliks": pereliks, "odvumirs": odvumirs})

@router.put("/material/{material_id}")
async def update_material(material_id: int, material: MaterialUpdate, db: Session = Depends(get_db)):
    db_material = db.query(Material).filter(Material.id == material_id).first()
    if not db_material:
        raise HTTPException(status_code=404, detail="Material not found")

    if material.weight is not None:
        db_material.weight = material.weight
    if material.notes is not None:
        db_material.notes = material.notes
    if material.id_perelik is not None:
        db_material.id_perelik = material.id_perelik
    if material.id_odvumir is not None:
        db_material.id_odvumir = material.id_odvumir

    db.commit()
    db.refresh(db_material)
    return db_material

@router.delete("/material/{material_id}")
async def delete_material(material_id: int, db: Session = Depends(get_db)):
    db_material = db.query(Material).filter(Material.id == material_id).first()
    if not db_material:
        raise HTTPException(status_code=404, detail="Material not found")
    db.delete(db_material)
    db.commit()
    return {"result": "Material deleted"}
