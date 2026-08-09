from fastapi import FastAPI
from app.routers import (admin, dashboard)
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from pathlib import Path
from app.database import Base, engine
from app.config import DEBUG_RESET_DB
# from app.services.analytics import dashboard_summary

# from app import models

BASE_DIR = Path(__file__).resolve().parent

# DEBUG_RESET_DB = False # True면 db에 있는 모든 자료를 삭제하고 초기화한다. config.py으로 이동.

if DEBUG_RESET_DB:
    print("=" * 60)
    print("Resetting database...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Database recreated.")
    print("=" * 60)

app = FastAPI(title="E-Commerce 3.1 (admin)")

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )

app.include_router(admin.router)
app.include_router(dashboard.router)
# app.include_router(products.router)
# app.include_router(customers.router)
# app.include_router(orders.router)
