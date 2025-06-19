from typing import Annotated, Optional
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, status
from pydantic import BaseModel, Field
from models import Users
from passlib.context import CryptContext
from database import SessionLocal 
from .auth import get_current_user


router = APIRouter(
    prefix= '/user',
    tags=['user']
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[Session, Depends(get_current_user)]


class PasswordRequest(BaseModel):
    password: str
    new_password: str
    
    
class ChangeRequest(BaseModel):
    first_name: str
    last_name:str
    email: str
    phone: str
    budget: int


@router.get('/', status_code=status.HTTP_200_OK)
async def get_user_details(db: db_dependency, 
                           user:user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    user_model = db.query(Users).filter(Users.id==user.get('id')).first()
    return user_model


@router.post('/edit', status_code=status.HTTP_204_NO_CONTENT)
async def edit_account_details(db: db_dependency, 
                               user:user_dependency, 
                               new_details: ChangeRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user_model=db.query(Users).filter(Users.id==user.get('id')).first()

    user_model.email = new_details.email
    user_model.first_name = new_details.first_name
    user_model.last_name = new_details.last_name
    user_model.phone = new_details.phone
    user_model.budget = new_details.budget
    
    db.add(user_model)
    db.commit()
    

@router.post('/change_password', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency,
                          db: db_dependency,
                          password_request: PasswordRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id==user.get('id')).first()

    if not bcrypt_context.verify(password_request.password, user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Error in password change')
    user_model.hashed_password = bcrypt_context.hash(password_request.new_password)
    db.add(user_model)
    db.commit()