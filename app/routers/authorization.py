from fastapi import APIRouter, Depends, HTTPException, status, Form, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse, HTMLResponse  
from fastapi.templating import Jinja2Templates
from app.models.users import Users
from app.database import get_db

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

@router.post("", response_class=HTMLResponse)
async def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.login == username).first()
    if not user or user.password != password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    elif user.role == 'admin':
        response = RedirectResponse(url="/index", status_code=303)
    elif user.role == 'workshop':
        response = RedirectResponse(url="/workshop/workshop_page", status_code=303)
    elif user.role == 'storage':
        response = RedirectResponse(url="/storage/storage_page", status_code=303)
    return response

