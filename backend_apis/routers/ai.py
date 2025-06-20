from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from models import Users
from database import SessionLocal
#from ai import run_model
from datetime import datetime
from .auth import get_current_user
from .insurelink_ai import insurance_recommendation, insurance_education
from .products import response

router = APIRouter(
    prefix= '/chat',
    tags=['chat']
)


def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency=Annotated[Session, Depends(get_current_user)]

class PromptRequest(BaseModel):
    message: str = Field(min_length=1)
    language: str
    
    
@router.post("/ask", status_code=status.HTTP_200_OK)
async def ai_response(user: user_dependency,
                      db: db_dependency, 
                      message: PromptRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    user_model = db.query(Users).filter(Users.id==user.get('id')).first()
    
    return insurance_education(message.message, message.language)
    


@router.post("/personalised_options", status_code=status.HTTP_200_OK)
async def ai_personalised_products(user: user_dependency,
                      db: db_dependency, 
                      ):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    user_model = db.query(Users).filter(Users.id==user.get('id')).first()
    
    user_data = {
    "name": user_model.first_name + user_model.last_name,
    "age": user_model.age,
    "budget":user_model.budget,
    "gender":user_model.gender,
    "type":"Give me a positive response from the insurance data sent to you."
}
    insurance_scheme = """[
  {
    "title": "AXA PRADO 1",
    "insurer_name": "AXA MANSARD",
    "insurer_logo": "https://www.axamansard.com/images/axa-logo.png",
    "product_type": "Life",
    "product_icon": "https://res.cloudinary.com/ddble5id6/image/upload/v1636627925/grow/life.svg",
    "price": 34,
    "price_unit": "NGN",
    "frequency": [
      "annually"
    ]
  },
  {
    "title": "Easy Care",
    "insurer_name": "AXA MANSARD",
    "insurer_logo": "https://www.axamansard.com/images/axa-logo.png",
    "product_type": "Health",
    "product_icon": "https://res.cloudinary.com/ddble5id6/image/upload/v1636627925/grow/health.svg",
    "price": 58446,
    "price_unit": "NGN",
    "frequency": [
      "annually"
    ]
  },
  {
    "title": "MEMPHIS CORE",
    "insurer_name": "Leadway",
    "insurer_logo": "https://www.leadway.com/wp-content/uploads/2019/07/logo-straight.png",
    "product_type": "Goods in Transit",
    "product_icon": null,
    "price": 33,
    "price_unit": "%",
    "frequency": [
      "annually"
    ]
  },
  {
    "title": "SMART INSURE LITE",
    "insurer_name": "Leadway",
    "insurer_logo": "https://www.leadway.com/wp-content/uploads/2019/07/logo-straight.png",
    "product_type": "Marine",
    "product_icon": null,
    "price": 0.25,
    "price_unit": "%",
    "frequency": [
      "annually"
    ]
  },
  {
    "title": "SMART INSURE PLUS",
    "insurer_name": "Leadway",
    "insurer_logo": "https://www.leadway.com/wp-content/uploads/2019/07/logo-straight.png",
    "product_type": "Life",
    "product_icon": "https://res.cloudinary.com/ddble5id6/image/upload/v1636627925/grow/life.svg",
    "price": 51,
    "price_unit": "NGN",
    "frequency": [
      "annually"
    ]
  },
  {
    "title": "Mutual Cover 2",
    "insurer_name": "OLD MUTUAL",
    "insurer_logo": "https://logonoid.com/images/old-mutual-logo.png",
    "product_type": "Marine",
    "product_icon": null,
    "price": 0.25,
    "price_unit": "%",
    "frequency": [
      "annually"
    ]
  },
  {
    "title": "Auto - Comprehensive Insurance (Saloon/SUVs)",
    "insurer_name": "AXA MANSARD",
    "insurer_logo": "https://www.axamansard.com/images/axa-logo.png",
    "product_type": "Comprehensive Auto",
    "product_icon": null,
    "price": 5,
    "price_unit": "%",
    "frequency": [
      "annually"
    ]
  },
  {
    "title": "3rd party motor",
    "insurer_name": "Tangerine Insurance",
    "insurer_logo": null,
    "product_type": "3rd Party Auto",
    "product_icon": "https://res.cloudinary.com/ddble5id6/image/upload/v1636627925/grow/auto.svg",
    "price": 15000,
    "price_unit": "NGN",
    "frequency": [
      "annually"
    ]
  },
  {
    "title": "GIT Retail 0-500,000",
    "insurer_name": "AXA MANSARD",
    "insurer_logo": "https://www.axamansard.com/images/axa-logo.png",
    "product_type": "Goods in Transit",
    "product_icon": null,
    "price": 0.2,
    "price_unit": "%",
    "frequency": [
      "annually"
    ]
  },
  {
    "title": "GIT Retail 500,001 - 1,000,000",
    "insurer_name": "Curacel Insur",
    "insurer_logo": "https://www.curacel.co/assets/img/Logo.svg",
    "product_type": "Goods in Transit",
    "product_icon": null,
    "price": 0.25,
    "price_unit": "%",
    "frequency": [
      "annually"
    ]
  },
  {
    "title": "Credit Life 001",
    "insurer_name": "AXA MANSARD",
    "insurer_logo": "https://www.axamansard.com/images/axa-logo.png",
    "product_type": "Credit Life",
    "product_icon": null,
    "price": null,
    "price_unit": "%",
    "frequency": [
      "annually"
    ]
  },
  {
    "title": "Marine Cargo Insurance",
    "insurer_name": "Cornerstone Insurance PLC",
    "insurer_logo": "https://cornerstone.com.ng/assets/img/logo.png",
    "product_type": "Marine",
    "product_icon": null,
    "price": 0.2,
    "price_unit": "%",
    "frequency": [
      "annually"
    ]
  },
  {
    "title": "Flexi Motor",
    "insurer_name": "Tangerine Insurance",
    "insurer_logo": null,
    "product_type": "Comprehensive Auto",
    "product_icon": null,
    "price": 5,
    "price_unit": "%",
    "frequency": [
      "annually"
    ]
  },
  {
    "title": "Heirs Save Plan",
    "insurer_name": "Heirs Insurance",
    "insurer_logo": null,
    "product_type": "Investment Life",
    "product_icon": null,
    "price": 0,
    "price_unit": "%",
    "frequency": [
      "annually"
    ]
  },
  {
    "title": "Mini Health Plan 2 (monthly)",
    "insurer_name": "Tangerine Insurance",
    "insurer_logo": null,
    "product_type": "Health",
    "product_icon": "https://res.cloudinary.com/ddble5id6/image/upload/v1636627925/grow/health.svg",
    "price": 1360,
    "price_unit": "NGN",
    "frequency": [
      "monthly"
    ]
  }
]
[
  {
    "title": "AXA PRADO 1",
    "insurer_name": "AXA MANSARD",
    "insurer_logo": "https://www.axamansard.com/images/axa-logo.png",
    "product_type": "Life",
    "product_icon": "https://res.cloudinary.com/ddble5id6/image/upload/v1636627925/grow/life.svg",
    "price": 34,
    "price_unit": "NGN",
    "frequency": [
      "annually"
    ]
  },
  {
    "title": "Easy Care",
    "insurer_name": "AXA MANSARD",
    "insurer_logo": "https://www.axamansard.com/images/axa-logo.png",
    "product_type": "Health",
    "product_icon": "https://res.cloudinary.com/ddble5id6/image/upload/v1636627925/grow/health.svg",
    "price": 58446,
    "price_unit": "NGN",
    "frequency": [
      "annually"
    ]
  },
  {
    "title": "MEMPHIS CORE",
    "insurer_name": "Leadway",
    "insurer_logo": "https://www.leadway.com/wp-content/uploads/2019/07/logo-straight.png",
    "product_type": "Goods in Transit",
    "product_icon": null,
    "price": 33,
    "price_unit": "%",
    "frequency": [
      "annually"
    ]
  },
  {
    "title": "SMART INSURE LITE",
    "insurer_name": "Leadway",
    "insurer_logo": "https://www.leadway.com/wp-content/uploads/2019/07/logo-straight.png",
    "product_type": "Marine",
    "product_icon": null,
    "price": 0.25,
    "price_unit": "%",
    "frequency": [
      "annually"
    ]
  },
  {
    "title": "SMART INSURE PLUS",
    "insurer_name": "Leadway",
    "insurer_logo": "https://www.leadway.com/wp-content/uploads/2019/07/logo-straight.png",
    "product_type": "Life",
    "product_icon": "https://res.cloudinary.com/ddble5id6/image/upload/v1636627925/grow/life.svg",
    "price": 51,
    "price_unit": "NGN",
    "frequency": [
      "annually"
    ]
  },
  {
    "title": "Mutual Cover 2",
    "insurer_name": "OLD MUTUAL",
    "insurer_logo": "https://logonoid.com/images/old-mutual-logo.png",
    "product_type": "Marine",
    "product_icon": null,
    "price": 0.25,
    "price_unit": "%",
    "frequency": [
      "annually"
    ]
  },
  {
    "title": "Auto - Comprehensive Insurance (Saloon/SUVs)",
    "insurer_name": "AXA MANSARD",
    "insurer_logo": "https://www.axamansard.com/images/axa-logo.png",
    "product_type": "Comprehensive Auto",
    "product_icon": null,
    "price": 5,
    "price_unit": "%",
    "frequency": [
      "annually"
    ]
  },
  {
    "title": "3rd party motor",
    "insurer_name": "Tangerine Insurance",
    "insurer_logo": null,
    "product_type": "3rd Party Auto",
    "product_icon": "https://res.cloudinary.com/ddble5id6/image/upload/v1636627925/grow/auto.svg",
    "price": 15000,
    "price_unit": "NGN",
    "frequency": [
      "annually"
    ]
  },
  {
    "title": "GIT Retail 0-500,000",
    "insurer_name": "AXA MANSARD",
    "insurer_logo": "https://www.axamansard.com/images/axa-logo.png",
    "product_type": "Goods in Transit",
    "product_icon": null,
    "price": 0.2,
    "price_unit": "%",
    "frequency": [
      "annually"
    ]
  },
  {
    "title": "GIT Retail 500,001 - 1,000,000",
    "insurer_name": "Curacel Insur",
    "insurer_logo": "https://www.curacel.co/assets/img/Logo.svg",
    "product_type": "Goods in Transit",
    "product_icon": null,
    "price": 0.25,
    "price_unit": "%",
    "frequency": [
      "annually"
    ]
  },
  {
    "title": "Credit Life 001",
    "insurer_name": "AXA MANSARD",
    "insurer_logo": "https://www.axamansard.com/images/axa-logo.png",
    "product_type": "Credit Life",
    "product_icon": null,
    "price": null,
    "price_unit": "%",
    "frequency": [
      "annually"
    ]
  },
  {
    "title": "Marine Cargo Insurance",
    "insurer_name": "Cornerstone Insurance PLC",
    "insurer_logo": "https://cornerstone.com.ng/assets/img/logo.png",
    "product_type": "Marine",
    "product_icon": null,
    "price": 0.2,
    "price_unit": "%",
    "frequency": [
      "annually"
    ]
  },
  {
    "title": "Flexi Motor",
    "insurer_name": "Tangerine Insurance",
    "insurer_logo": null,
    "product_type": "Comprehensive Auto",
    "product_icon": null,
    "price": 5,
    "price_unit": "%",
    "frequency": [
      "annually"
    ]
  },
  {
    "title": "Heirs Save Plan",
    "insurer_name": "Heirs Insurance",
    "insurer_logo": null,
    "product_type": "Investment Life",
    "product_icon": null,
    "price": 0,
    "price_unit": "%",
    "frequency": [
      "annually"
    ]
  },
  {
    "title": "Mini Health Plan 2 (monthly)",
    "insurer_name": "Tangerine Insurance",
    "insurer_logo": null,
    "product_type": "Health",
    "product_icon": "https://res.cloudinary.com/ddble5id6/image/upload/v1636627925/grow/health.svg",
    "price": 1360,
    "price_unit": "NGN",
    "frequency": [
      "monthly"
    ]
  }
]"""
    return {
        "reccomendations": insurance_recommendation(user_data, insurance_scheme, language='english')
    }