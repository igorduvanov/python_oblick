from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

@router.get("/storage_page", response_class=HTMLResponse)
async def storage_page(request: Request):
    return templates.TemplateResponse("storage_page.html", {"request": request})
