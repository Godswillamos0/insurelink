<<<<<<< HEAD:backend_apis/routers/customer_service.py
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from models import Users, InsuranceProduct, Premium, Claims
from database import SessionLocal
#from ai import run_model
from datetime import datetime
from .auth import get_current_user
from .ai_model import chat
import os


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
    
    
@router.post("/chat", status_code=status.HTTP_200_OK)
async def ai_response(user: user_dependency,
                      db: db_dependency, 
                      message: PromptRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    user_model = db.query(Users).filter(Users.id==user.get('id')).first()
    
    return chat(message.message)
    

