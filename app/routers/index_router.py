from fastapi import APIRouter, Request, Depends  
from fastapi.responses import HTMLResponse
from app.routers.dependencies import get_current_user
from app.models.users import Users
from app.templates import templates


router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def read_index(request: Request, current_user: Users = Depends(get_current_user)):
    if current_user.role == 'admin':
        return templates.TemplateResponse("/templates/index.html", {"request": request})
    elif current_user.role == 'workshop':
        return templates.TemplateResponse("/templates/workshop_page.html", {"request": request})
    elif current_user.role == 'storage':
        return templates.TemplateResponse("/templates/storage_page.html", {"request": request})
    else:
        raise HTTPException(status_code=403, detail="Access forbidden")

