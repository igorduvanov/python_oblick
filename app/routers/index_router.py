from fastapi import APIRouter, Request, Depends  
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.routers.dependencies import get_current_user
from app.models.users import Users

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def read_index(request: Request, current_user: Users = Depends(get_current_user)):
    if current_user.role == 'admin':
        return templates.TemplateResponse("index.html", {"request": request})
    elif current_user.role == 'workshop':
        return templates.TemplateResponse("workshop_page.html", {"request": request})
    elif current_user.role == 'storage':
        return templates.TemplateResponse("storage_page.html", {"request": request})
    else:
        raise HTTPException(status_code=403, detail="Access forbidden")

