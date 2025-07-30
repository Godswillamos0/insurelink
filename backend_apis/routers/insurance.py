from typing import Annotated, Optional
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field
from database import SessionLocal
from sqlalchemy.orm import Session
from models import Premium, InsuranceProduct, Users, Claims
from .auth import get_current_user
from datetime import datetime, timedelta
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

'''
@router.get('/products', status_code=status.HTTP_200_OK)
async def get_all_product(db: db_dependency, user:user_dependency):
    
    return extract_important_insurance_details()
'''
<<<<<<< HEAD

class Insurance(BaseModel):
    insurance_type: str = Field(min_length=1, max_length=50)
    start_time: str = Field(min_length=1, max_length=50)
    end_time: str = Field(min_length=1, max_length=50)
    amount: Optional[int] = Field(gt=299, default=300)  # Default amount if not provided
    #owner_id: int = Field(gt=0)


@router.post('/buy', status_code=status.HTTP_201_CREATED)
async def buy_insurance(db: db_dependency, user: user_dependency,
                        insurance: Insurance):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")           
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found") 
    insurance_model = InsuranceProduct(
        owner_id=user_model.id,
        start_time=insurance.start_time,
        end_time=insurance.end_time,
        amount=insurance.amount, 
        insurance_type=insurance.insurance_type
    )
    db.add(insurance_model)
    db.commit()  
    
    return {"message": "Insurance purchased successfully", "insurance_id": insurance_model.id} 


class PremiumPayment(BaseModel):
    insurance_id: int = Field(gt=0, description="ID of the insurance product to pay premium for")
    
    
    
@router.get('/all', status_code=status.HTTP_201_CREATED)
async def get_all_insurance_products(db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    
    insurance_products = db.query(InsuranceProduct).filter(InsuranceProduct.owner_id == user.get('id')).all()
    if not insurance_products:  
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No insurance products found for this user")
    # Extracting only the necessary fields
    
    return insurance_products


@router.get('/premium', status_code=status.HTTP_200_OK)
async def get_premium_details(db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    
    premiums = db.query(Premium).filter(Premium.owner_id == user.get('id')).all()
    if not premiums:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No premium details found for this user")
    
    return premiums


@router.post('/pay_premium', status_code=status.HTTP_200_OK)
async def pay_premium(db: db_dependency, user: user_dependency,
                      premium: PremiumPayment):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    insurance_model = db.query(InsuranceProduct).filter(InsuranceProduct.id == premium.insurance_id).first()
    if insurance_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Insurance not found")
    
    premium_model = Premium(
        owner_id=user_model.id,
        insurance_id=insurance_model.id,
        amount=insurance_model.amount,
        due_date=datetime.now() + timedelta(days=30),  # Assuming a 30-day payment period
        is_paid=True,  # Assuming the payment is made immediately
        paid_date=datetime.now()
    )
    
    db.add(premium_model)
    db.commit()
    
    webbrowser.open("https://paystack.shop/pay/insurelink")
    
    return {"message": "Premium payment initiated", "premium_id": premium_model.id}


@router.get('/claims', status_code=status.HTTP_200_OK)
async def get_claims(db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    
    claims = db.query(Claims).filter(Claims.owner_id == user.get('id')).all()
    if not claims:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No claims found for this user")
    
    return claims


@router.post('/claim', status_code=status.HTTP_201_CREATED)
async def file_claim(db: db_dependency, user: user_dependency, insurance_id: int):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    insurance_model = db.query(InsuranceProduct).filter(InsuranceProduct.id == insurance_id).first()
    if insurance_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Insurance not found")
    
    claim_model = Claims(
        owner_id=user_model.id,
        insurance_id=insurance_model.id,
        document_submitted=True,  # Assuming document submission is handled separately
        document_verified=False
    )
    
    db.add(claim_model)
    db.commit()
    
    return {"message": "Claim filed successfully", "claim_id": claim_model.id}
=======
>>>>>>> 7ecf3efc9f28548cbb7482df0834d54f9974401f
    

@router.get('/pay', status_code=status.HTTP_200_OK)
async def pay_for_product(user:user_dependency):
    
    pass