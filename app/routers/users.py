from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from app.models.users import Users
from app.database import get_db
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from fastapi.responses import HTMLResponse
from app.templates import templates

router = APIRouter()

class UserBase(BaseModel):
    login: str
    password: str
    role: str
    notes: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    login: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    notes: Optional[str] = None

class UserInDB(UserBase):
    id: int
    date_created: Optional[str] = None
    date_updated: Optional[str] = None

    class Config:
        orm_mode = True

class UserOut(BaseModel):
    id: int
    login: str
    password: str
    role: str
    notes: str
    date_created: datetime
    date_updated: datetime

def create_user_in_db(user: UserCreate, db: Session):
    new_user = Users(login=user.login, password=user.password, role=user.role, notes=user.notes)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/users/")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = create_user_in_db(user, db)
    return new_user

@router.get("/users_page", response_class=HTMLResponse)
async def read_users_page(request: Request, db: Session = Depends(get_db), search: Optional[str] = None, sort_by: Optional[str] = None):
    users = db.query(Users)

    if search:
        users = users.filter(Users.login.contains(search))

    if sort_by:
        if sort_by == "year_asc":
            users = users.order_by(Users.date_created.asc())
        elif sort_by == "year_desc":
            users = users.order_by(Users.date_created.desc())

    users = users.all()

    return templates.TemplateResponse("users_page.html", {"request": request, "users": users, "search": search, "sort_by": sort_by})

@router.put("/users/{user_id}")
async def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(Users).filter(Users.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.login is not None:
        db_user.login = user.login
    if user.password is not None:
        db_user.password = user.password
    if user.role is not None:
        db_user.role = user.role
    if user.notes is not None:
        db_user.notes = user.notes
    
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(Users).filter(Users.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"detail": "User deleted"}
