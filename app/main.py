from fastapi.responses import HTMLResponse
from app.routers import odvumir, oper, robitnuk, perelik, material, price, nakladna, operation, resur, marshryt, denzvit, unit, users, authorization
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from app.templates import templates
from app.workshop.workshop_routers import router as workshop_router
from app.storage.storage_routers import router as storage_router
from app.routers.index_router import router as index_router

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")
#головна сторінка за замовчуванням
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("auth_page.html", {"request": request})

#css
app.mount("/static", StaticFiles(directory="app/static"), name="static")
# роутери на CRUD
app.include_router(odvumir.router, prefix="/odvumir", tags=["odvumir"])
app.include_router(oper.router, prefix="/oper", tags=["oper"])
app.include_router(robitnuk.router, prefix="/robitnuk", tags=["robitnuk"])
app.include_router(perelik.router, prefix="/perelik", tags=["perelik"])
app.include_router(material.router, prefix="/material", tags=["material"])
app.include_router(price.router, prefix="/price", tags=["price"])
app.include_router(nakladna.router, prefix="/nakladna", tags=["nakladna"])
app.include_router(unit.router, prefix="/unit", tags=["unit"])
app.include_router(operation.router, prefix="/operation", tags=["operation"])
app.include_router(resur.router, prefix="/resur", tags=["resur"])
app.include_router(marshryt.router, prefix="/marshryt", tags=["marshryt"])
app.include_router(denzvit.router, prefix="/denzvit", tags=["denzvit"])
app.include_router(users.router, prefix="/users", tags=["users"])
#роутер авторизації
app.include_router(authorization.router, prefix="/login")
app.include_router(index_router, prefix="/index")
app.include_router(workshop_router, prefix="/workshop")
app.include_router(storage_router, prefix="/storage")

