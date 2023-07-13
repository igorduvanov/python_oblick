from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Request, Depends, HTTPException, status, Body
from fastapi.responses import HTMLResponse
from app.routers.dependencies import get_current_user
from app.models.users import Users
from sqlalchemy.orm import Session
from app.database import get_db
from app.templates import templates
from app.models import Robitnuk, Operation, Odvumir, Oper
from app.models.denzvit import Denzvit
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter()

class DenzvitBase(BaseModel):
    id_robitnuk: int
    id_operation: int
    kilkist: int
    id_odvumir: Optional[int] = None


class DenzvitCreate(BaseModel):
    id_robitnuk: List[int]
    id_operation: List[int]
    kilkist: List[int]
    id_odvumir: List[Optional[int]]


def create_denzvit_in_db(denzvit: DenzvitCreate, db: Session):
    new_denzvits = []
    for i in range(len(denzvit.id_robitnuk)):
        new_denzvit = Denzvit(id_robitnuk=denzvit.id_robitnuk[i], id_operation=denzvit.id_operation[i],
                              kilkist=denzvit.kilkist[i], id_odvumir=denzvit.id_odvumir[i])
        db.add(new_denzvit)
        new_denzvits.append(new_denzvit)
    try:
        db.commit()
    except SQLAlchemyError as e:
        print("Failed to add new denzvit to the database.")
        print(e)
        db.rollback()
        return []
    for new_denzvit in new_denzvits:
        db.refresh(new_denzvit)
    return new_denzvits

@router.post("/workshop/workshop_denzvit_form", status_code=status.HTTP_201_CREATED)
async def process_denzvit_form(
    denzvit: DenzvitCreate = Body(...),
    db: Session = Depends(get_db)
    ):
    new_denzvits = create_denzvit_in_db(denzvit, db)
    return new_denzvits


@router.get("/workshop_denzvit_form", response_class=HTMLResponse)
async def read_index(request: Request, current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    robitnuks = db.query(Robitnuk).all()
    operations = db.query(Operation).join(Oper).all()
    odvumirs = db.query(Odvumir).all()
    return templates.TemplateResponse("workshop/workshop_templates/workshop_denzvit_form.html",
                                      {"request": request, "robitnuks": robitnuks, "operations": operations, "odvumirs": odvumirs})
