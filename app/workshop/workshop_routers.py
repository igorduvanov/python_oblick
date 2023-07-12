from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

@router.get("/workshop_page", response_class=HTMLResponse)
async def workshop_page(request: Request):
    return templates.TemplateResponse("workshop_page.html", {"request": request})
