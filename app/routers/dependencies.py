from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status, Cookie
from app.models.users import Users
from sqlalchemy.orm import Session
from app.database import get_db
from app.routers.authorization import SECRET_KEY, ALGORITHM
from pydantic import BaseModel

class TokenData(BaseModel):
    username: str
    role: str

async def get_current_user(db: Session = Depends(get_db), token: str = Cookie(None, alias="accessToken")):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        raise credentials_exception

    try:
       
        token_parts = token.split()
        if len(token_parts) == 2:
            token = token_parts[1]
        elif len(token_parts) == 1:
            token = token_parts[0] 
        else:
            print(f"Could not split token: {token}")
            raise credentials_exception


        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, role=role)
    except JWTError:
        raise credentials_exception

    user = db.query(Users).filter(Users.login == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user
