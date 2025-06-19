from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field
from database import SessionLocal
from sqlalchemy.orm import Session
from models import Datas
from .auth import get_current_user
from datetime import datetime, timedelta
from .products import extract_important_insurance_details
import webbrowser


router = APIRouter(
    tags=['Insurance'],
    prefix='/insurance'
)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[Session, Depends(get_current_user)]


@router.get('/products', status_code=status.HTTP_200_OK)
async def get_all_product(db: db_dependency, user:user_dependency):
    
    return extract_important_insurance_details()
    

@router.get('/pay', status_code=status.HTTP_200_OK)
async def pay_for_product(user:user_dependency):
    
    webbrowser.open("https://paystack.shop/pay/insurelink")