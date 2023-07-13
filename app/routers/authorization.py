from jose import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status, APIRouter, Form, Response
from sqlalchemy.orm import Session
from app.models import Users   
from pydantic import BaseModel
from app.database import get_db

SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()  
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

class Token(BaseModel):  
    access_token: str
    token_type: str

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("", response_model=Token)
async def login_for_access_token(response: Response, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.login == username).first()
    if not user or user.password != password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.login, "role": user.role})
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True, max_age=1800)
    return {"access_token": access_token, "token_type": "bearer"}

