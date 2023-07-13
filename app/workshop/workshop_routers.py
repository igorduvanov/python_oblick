from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from app.routers.dependencies import get_current_user
from app.models.users import Users
from app.routers.denzvit import DenzvitCreate, create_denzvit_in_db
from sqlalchemy.orm import Session
from app.database import get_db
from app.templates import templates

router = APIRouter()


@router.get("/workshop_page", response_class=HTMLResponse)
async def read_index(request: Request, current_user: Users = Depends(get_current_user)):
    if current_user.role == 'admin':
        return templates.TemplateResponse("/templates/index.html", {"request": request})
    elif current_user.role == 'workshop':
        return templates.TemplateResponse("/templates/workshop_page.html", {"request": request})
    elif current_user.role == 'storage':
        return templates.TemplateResponse("/templates/storage_page.html", {"request": request})
    else:
        raise HTTPException(status_code=403, detail="Access forbidden")

@router.get("/workshop_denzvit_form", response_class=HTMLResponse)
async def get_denzvit_form(request: Request, current_user: Users = Depends(get_current_user)):
    if current_user.role == 'workshop':
        return templates.TemplateResponse("workshop/workshop_templates/workshop_denzvit_form.html", {"request": request})
    else:
        raise HTTPException(status_code=403, detail="Access forbidden")
        
@router.post("/workshop_denzvit_form", response_model=DenzvitCreate)
async def post_denzvit_form(denzvit: DenzvitCreate, db: Session = Depends(get_db)):
    new_denzvit = create_denzvit_in_db(denzvit, db)
    return new_denzvit
