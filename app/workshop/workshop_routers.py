from typing import Optional, Dict, List
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from app.routers.dependencies import get_current_user
from app.models.users import Users
from sqlalchemy.orm import Session
from app.database import get_db
from app.templates import templates
from app.models import Robitnuk, Operation, Odvumir, Oper
from app.models.denzvit import Denzvit
from pydantic import BaseModel

router = APIRouter()

class DenzvitBase(BaseModel):
    id_robitnuk: List[int]
    id_operation: List[int]
    kilkist: List[int]
    id_odvumir: List[Optional[int]]

class DenzvitCreate(DenzvitBase):
    pass

def create_denzvit_in_db(denzvit: DenzvitCreate, db: Session):
    for i in range(len(denzvit.id_robitnuk)):
        new_denzvit = Denzvit(id_robitnuk=denzvit.id_robitnuk[i], id_operation=denzvit.id_operation[i],
                              kilkist=denzvit.kilkist[i], id_odvumir=denzvit.id_odvumir[i])
        db.add(new_denzvit)
    db.commit()

@router.post("/workshop/workshop_denzvit_form")
async def create_denzvit(denzvit: DenzvitCreate, db: Session = Depends(get_db)):
    create_denzvit_in_db(denzvit, db)
    return {"status": "success"}

@router.get("/workshop_denzvit_form", response_class=HTMLResponse)
async def read_index(request: Request, db: Session = Depends(get_db)):
    robitnuks = db.query(Robitnuk).all()
    operations = db.query(Operation).join(Oper).all()
    odvumirs = db.query(Odvumir).all()
    return templates.TemplateResponse("workshop/workshop_templates/workshop_denzvit_form.html",
                                      {"request": request, "robitnuks": robitnuks, "operations": operations, "odvumirs": odvumirs})
