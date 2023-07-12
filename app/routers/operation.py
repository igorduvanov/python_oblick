from app.models.perelik import Perelik
from app.models.oper import Oper
from app.models.operation import Operation
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from app.database import get_db
from app.templates import templates
router = APIRouter()

class OperationBase(BaseModel):
    id_perelik: int
    id_oper: int

class OperationCreate(OperationBase):
    pass

class OperationUpdate(OperationBase):
    id_perelik: Optional[int] = None
    id_oper: Optional[int] = None

class OperationInDB(OperationBase):
    id: int
    date_created: Optional[str] = None
    date_updated: Optional[str] = None

    class Config:
        orm_mode = True

class OperationOut(BaseModel):
    id: int
    id_perelik: int
    id_oper: int
    date_created: datetime
    date_updated: datetime

def create_operation_in_db(operation: OperationCreate, db: Session):
    new_operation = Operation(
        id_perelik=operation.id_perelik, 
        id_oper=operation.id_oper, 
        date_created=datetime.utcnow(), 
        date_updated=datetime.utcnow()
    )
    db.add(new_operation)
    db.commit()
    db.refresh(new_operation)
    return new_operation


@router.post("/operation/")
async def create_operation(operation: OperationCreate, db: Session = Depends(get_db)):
    new_operation = create_operation_in_db(operation, db)
    return new_operation

@router.get("/operation_page", response_class=HTMLResponse)
async def read_operation_page(request: Request, db: Session = Depends(get_db), search: Optional[str] = None,
                            sort_by: Optional[str] = None):
    operations = db.query(Operation).all()

    pereliks = db.query(Perelik).all()
    opers = db.query(Oper).all()

    if search:
        operations = db.query(Operation).join(Perelik).filter(Perelik.coding.contains(search)).all()

    if sort_by:
        if sort_by == "year_asc":
            operations = operations.order_by(Operation.date_created.asc())
        elif sort_by == "year_desc":
            operations = operations.order_by(Operation.date_created.desc())

    return templates.TemplateResponse("operation_page.html",
                                      {"request": request, "operations": operations, "search": search, "sort_by": sort_by,
                                       "pereliks": pereliks, "opers": opers})

@router.put("/operation/{operation_id}")
async def update_operation(operation_id: int, operation: OperationUpdate, db: Session = Depends(get_db)):
    db_operation = db.query(Operation).filter(Operation.id == operation_id).first()
    if not db_operation:
        raise HTTPException(status_code=404, detail="Operation not found")

    if operation.id_perelik is not None:
        db_operation.id_perelik = operation.id_perelik
    if operation.id_oper is not None:
        db_operation.id_oper = operation.id_oper

    db.commit()
    db.refresh(db_operation)
    return db_operation

@router.delete("/operation/{operation_id}")
async def delete_operation(operation_id: int, db: Session = Depends(get_db)):
    db_operation = db.query(Operation).filter(Operation.id == operation_id).first()
    if not db_operation:
        raise HTTPException(status_code=404, detail="Operation not found")
    db.delete(db_operation)
    db.commit()
    return {"detail": "Operation deleted"}
