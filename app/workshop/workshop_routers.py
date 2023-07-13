from typing import Optional
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
    id_robitnuk: int
    id_operation: int
    kilkist: int
    id_odvumir: Optional[int] = None


class DenzvitCreate(DenzvitBase):
    pass

def create_denzvit_in_db(denzvit: DenzvitCreate, db: Session):
    new_denzvit = Denzvit(id_robitnuk=denzvit.id_robitnuk, id_operation=denzvit.id_operation,
                          kilkist=denzvit.kilkist, id_odvumir=denzvit.id_odvumir)
    db.add(new_denzvit)
    db.commit()
    db.refresh(new_denzvit)
    return new_denzvit

@router.post("/workshop/workshop_denzvit_form")
async def create_denzvit(denzvit: DenzvitCreate, db: Session = Depends(get_db)):
    new_denzvit = create_denzvit_in_db(denzvit, db)
    return new_denzvit

@router.get("/workshop_denzvit_form", response_class=HTMLResponse)
async def read_index(request: Request, db: Session = Depends(get_db)):
    robitnuks = db.query(Robitnuk).all()
    operations = db.query(Operation).join(Oper).all()
    odvumirs = db.query(Odvumir).all()
    return templates.TemplateResponse("workshop/workshop_templates/workshop_denzvit_form.html",
                                      {"request": request, "robitnuks": robitnuks, "operations": operations, "odvumirs": odvumirs})
