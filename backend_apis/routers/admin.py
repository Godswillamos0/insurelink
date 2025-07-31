from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel, Field
from database import SessionLocal
from sqlalchemy.orm import Session
from models import InsuranceProduct, Claims, Users
from datetime import datetime, timedelta


router = APIRouter(
    tags=['admin'],
    prefix='/admin'
)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.get('/products', status_code=status.HTTP_200_OK)
async def get_all_products(db: db_dependency):  
    products = db.query(InsuranceProduct).all()
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No insurance products found")
    
    return products


@router.get('/claims', status_code=status.HTTP_200_OK)
async def get_all_claims(db: db_dependency):
    claims = db.query(Claims).all()
    if not claims:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No claims found")
    
    return claims


@router.get('/users', status_code=status.HTTP_200_OK)
async def get_all_users(db: db_dependency):
    users = db.query(Users).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
    
    return users


@router.post('/verify_claim/{claim_id}', status_code=status.HTTP_200_OK)
async def verify_claim(db: db_dependency, claim_id: int):
    claim = db.query(Claims).filter(Claims.id == claim_id).first()
    if not claim:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Claim not found")
    
    # Assuming some verification logic here
    claim.document_verified = True
    db.commit()
    
    return {"message": "Claim verified successfully", "claim_id": claim.id}