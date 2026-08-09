from fastapi import APIRouter, Depends
from app.dependencies import get_db
from sqlalchemy.orm import Session
# from app.config import DEBUG_RESET_DB
# from app.services.data_generator import generate_fake_data
# from app.services.load_data_from_db import load_from_db
from app.services.analytics import dashboard_summary, monthly_sales, piechart_categories, barchart_cities

router = APIRouter()

@router.get("/dashboard/summary")
def get_summary(city: str | None = None, category: str | None = None, db: Session = Depends(get_db)):
    return dashboard_summary(db, city, category)


@router.get("/dashboard/monthly_sales")
def get_monthly_sales(city: str | None = None, category: str | None = None, db: Session = Depends(get_db)):
    return monthly_sales(db, city)

@router.get("/dashboard/piechart_categories")
def get_piechart(city: str | None = None, db: Session = Depends(get_db)):
    return piechart_categories(db, city)

@router.get("/dashboard/barchart_cities")
def get_barchart(category: str | None = None, db: Session = Depends(get_db)):
    return barchart_cities(db, category)
