from fastapi.responses import HTMLResponse
from fastapi import FastAPI
from app.routers import odvumir, oper, robitnuk, perelik, material, price, nakladna, operation, resur, marshryt, denzvit
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import Depends
from app.database import SessionLocal
from app.models.odvumir import Odvumir


app = FastAPI()

# Add this function to handle the database sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

templates = Jinja2Templates(directory="app/templates")

@app.get("/")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

class OdvumirCreate(BaseModel):
    name: str
    notes: str

@app.post("/odvumir/")
async def create_odvumir(odvumir: OdvumirCreate, db: Session = Depends(get_db)):
    new_odvumir = Odvumir(name=odvumir.name, notes=odvumir.notes)
    db.add(new_odvumir)
    db.commit()
    db.refresh(new_odvumir)
    return new_odvumir

app.include_router(odvumir.router, prefix="/odvumir", tags=["odvumir"])
#app.include_router(oper.router, prefix="/oper", tags=["oper"])
#app.include_router(robitnuk.router, prefix="/robitnuk", tags=["robitnuk"])
#app.include_router(perelik.router, prefix="/perelik", tags=["perelik"])
#app.include_router(material.router, prefix="/material", tags=["material"])
#app.include_router(price.router, prefix="/price", tags=["price"])
#app.include_router(nakladna.router, prefix="/nakladna", tags=["nakladna"])
#app.include_router(operation.router, prefix="/operation", tags=["operation"])
#app.include_router(resur.router, prefix="/resur", tags=["resur"])
#app.include_router(marshryt.router, prefix="/marshryt", tags=["marshryt"])
#app.include_router(denzvit.router, prefix="/denzvit", tags=["denzvit"])
