from fastapi import APIRouter, Depends
from app.dependencies import get_db
from sqlalchemy.orm import Session
from app.services.data_generator import generate_fake_data
# from app.services.data_loader import dump_to_db
from app.services.analytics import analyse #, test_analyze
from app.config import DEBUG_RESET_DB
# from app.services.load_data_from_db import load_from_db

router = APIRouter()

@router.post("/admin/generate_data")
def generate_data(db: Session = Depends(get_db)):

    if DEBUG_RESET_DB:
        world = generate_fake_data(customer_count = 567,
                                   product_count = (5,6),
                                   order_count = 8901,
                                   city_count = 5)
        db.add_all(world.customers)  # 이 둘만 추가해도 됨.
        db.add_all(world.categories)  # 이 둘만 추가해도 됨.
        db.commit()
    else:
        analyse(db)
