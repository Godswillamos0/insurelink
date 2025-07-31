from typing import Annotated
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect, UploadFile, File
from fastapi.responses import HTMLResponse
import io
import os
from pathlib import Path
from pydub import AudioSegment
import asyncio
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from models import Users, InsuranceProduct, Premium, Claims
from database import SessionLocal
#from ai import run_model
from datetime import datetime
from .auth import get_current_user
from .ai_model import chat

"""from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import io
import openai
from pydub import AudioSegment
import asyncio"""


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
    
    
@router.post("/app", status_code=status.HTTP_200_OK)
async def ai_response(user: user_dependency,
                      db: db_dependency, 
                      message: PromptRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    user_model = db.query(Users).filter(Users.id==user.get('id')).first()
    
    return chat(message.message)


@router.post("/tel_bot", status_code=status.HTTP_200_OK)
async def tel_bot_chat(request: PromptRequest):
    result = chat(request.message)
    return {"response": result}
   
    
    

