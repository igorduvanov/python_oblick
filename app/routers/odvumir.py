from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.odvumir import Odvumir
from app.schemas import OdvumirCreate, OdvumirUpdate, OdvumirInDB
from app.database import get_db
from typing import List

router = APIRouter()

# Create
@router.post("/", response_model=OdvumirInDB)
def create_odvumir(odvumir: OdvumirCreate, db: Session = Depends(get_db)):
    new_odvumir = Odvumir(**odvumir.dict())
    db.add(new_odvumir)
    db.commit()
    db.refresh(new_odvumir)
    return new_odvumir

# Read
@router.get("/{odvumir_id}", response_model=OdvumirInDB)
def get_odvumir(odvumir_id: int, db: Session = Depends(get_db)):
    odvumir = db.query(Odvumir).filter(Odvumir.id == odvumir_id).first()
    if not odvumir:
        raise HTTPException(status_code=404, detail="Odvumir not found")
    return odvumir

# Update
@router.put("/{odvumir_id}", response_model=OdvumirInDB)
def update_odvumir(odvumir_id: int, odvumir: OdvumirUpdate, db: Session = Depends(get_db)):
    db_odvumir = db.query(Odvumir).filter(Odvumir.id == odvumir_id).first()
    if not db_odvumir:
        raise HTTPException(status_code=404, detail="Odvumir not found")

    for key, value in odvumir.dict().items():
        if value is not None:
            setattr(db_odvumir, key, value)

    db.commit()
    db.refresh(db_odvumir)
    return db_odvumir

# Delete
@router.delete("/{odvumir_id}", response_model=int)
def delete_odvumir(odvumir_id: int, db: Session = Depends(get_db)):
    db_odvumir = db.query(Odvumir).filter(Odvumir.id == odvumir_id).first()
    if not db_odvumir:
        raise HTTPException(status_code=404, detail="Odvumir not found")

    db.delete(db_odvumir)
    db.commit()
    return odvumir_id

# List all
@router.get("/", response_model=List[OdvumirInDB])
def list_odvumirs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    odvumirs = db.query(Odvumir).offset(skip).limit(limit).all()
    return odvumirs
