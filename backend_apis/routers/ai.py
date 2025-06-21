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
import json

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
    with open("data.json", "r") as f:
        insurance_data = json.load(f)

# Convert to string
    insurance_str = json.dumps(insurance_data)
    return {
        "reccomendations": insurance_recommendation(user_data, insurance_str, language='english')
    }
