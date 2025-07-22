from datetime import datetime, timedelta, timezone
import re
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError, jwt
from pydantic import BaseModel, Field, EmailStr
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from dotenv import load_dotenv
import os
import httpx
from pathlib import Path
import random


env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


load_dotenv()  # Loads from .env into environment variables



SECRET_KEY = os.get_env("SECRET_KEY")
ALGORITHM = os.get_env("ALGORITHM")

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get('sub')
        user_id: int = payload.get('id')
        #user_role:str = payload.get('role')
        if email is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')
        return {'email': email, 
                'id': user_id, 
                #'user_role': user_role
                }
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')
        
        
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[Session, Depends(get_current_user)]


TERMII_API_KEY = os.get_env("TERMII_API_KEY")
CONFIG_ID = os.get_env("CONFIG_ID")


async def send_email_otp(email: str, code: str):
    url = "https://api.ng.termii.com/api/email/otp/send"
    payload = {
        "api_key": TERMII_API_KEY,
        "email_address": email,
        "code": code,
        "email_configuration_id": CONFIG_ID
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=payload)
        return resp.json()
        
        
otp_store = {}

def generate_otp():
    return str(random.randint(100000, 999999))
        
        
class CreateUserRequest(BaseModel):
    first_name:str=Field(min_length=3, max_length=50)
    last_name:str = Field(min_length=3, max_length=50)
    email: str 
    password:str
    phone:str
    email_verified: Optional[bool]= False
    is_onboarded: Optional[bool] = False
    
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "johndoe@mail.com",
                "password": "strongpassword123",
                "phone": "+1234567890",
            }
        }
    }
    

class Token(BaseModel):
    access_token:str
    token_type:str
    

class EmailRequest(BaseModel):
    email: EmailStr
    code: str = None
    
    
class PasswordRequest(BaseModel):
    email: EmailStr
    new_password: str
    
    
@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,
                      create_user_request: CreateUserRequest):
    create_user_model = Users(
        email = create_user_request.email,
        first_name =  create_user_request.first_name,
        last_name=  create_user_request.last_name,
        hashed_password = bcrypt_context.hash(create_user_request.password),
        phone= create_user_request.phone
    )
    
    db.add(create_user_model)
    db.commit()
    

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency):
    # Treat the 'username' field as the email address
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid email or password.'
        )

    if not user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Email not verified.'
        )

    token = create_access_token(user.email, user.id, timedelta(hours=1))
    return {'access_token': token, 'token_type': 'bearer'}


def create_access_token(email:str, 
                        user_id: int, 
                        expires_delta: timedelta):
    encode = {
        'sub': email,
        'id': user_id,
    }
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def authenticate_user(email: str, password: str, db: Session):
    user = db.query(Users).filter(Users.email == email).first()
  #  else:
       # user = db.query(Users).filter(Users.username == username_or_email).first()

    if not user or not bcrypt_context.verify(password, user.hashed_password):
        return False

    return user


@router.post("/confirm-email/")
async def confirm_email(data: EmailRequest, db: db_dependency):
    
    email = str(data.email)
    user_model = db.query(Users).filter(Users.email == email).first()
    
    if not user_model:
        raise HTTPException(status_code=404, detail="User not found")    
    
    if user_model.email_verified:
        raise HTTPException(status_code=400, detail="Email already verified")
    
    otp = generate_otp()
    otp_store[data.email] = (otp, datetime.utcnow())
    resp = await send_email_otp(data.email, otp)
    
    return {"status": resp}
    
    
@router.post("/forgot-password-otp/")
async def send_forgot_password_otp(data: EmailRequest, db: db_dependency):
    user = db.query(Users).filter(Users.email == data.email).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    otp = generate_otp()
    otp_store[data.email] = (otp, datetime.utcnow())
    resp = await send_email_otp(data.email, otp)
    
    return {"status": resp}


@router.post("/verify-email-otp/")
async def verify_email(data: EmailRequest, db: db_dependency):
        
    user_model = db.query(Users).filter(Users.email == data.email).first()
        
    entry = otp_store.get(data.email)
    if not entry:
        raise HTTPException(status_code=400, detail="No OTP found")

    otp, timestamp = entry
    if datetime.utcnow() > timestamp + timedelta(minutes=5):
        del otp_store[data.email]
        raise HTTPException(status_code=400, detail="OTP expired")

    if data.code != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    del otp_store[data.email]

    user_model.email_verified = True
    db.commit()
    
    return {"verified": True}


@router.post("/verify-password-otp/")
async def forgot_password_verification(data: PasswordRequest, db: db_dependency):
        
    user_model = db.query(Users).filter(Users.email == data.email).first()
        
    entry = otp_store.get(data.email)
    if not entry:
        raise HTTPException(status_code=400, detail="No OTP found")

    otp, timestamp = entry
    if datetime.utcnow() > timestamp + timedelta(minutes=5):
        del otp_store[data.email]
        raise HTTPException(status_code=400, detail="OTP expired")

    if data.code != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    del otp_store[data.email]

    user_model.hashed_password = bcrypt_context.hash(data.new_password)
    db.commit()
    
    return {"changed_password": True}


# @router.post('/forgot_password', status_code=status.HTTP_204_NO_CONTENT)
# async def change_password(db: db_dependency,):
#     user_model = db.query(Users).filter(Users.id==user.get('id')).first()

#     if not bcrypt_context.verify(password_request.password, user_model.hashed_password):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Error in password change')
#     user_model.hashed_password = bcrypt_context.hash(password_request.new_password)
#     db.add(user_model)
#     db.commit()
    

