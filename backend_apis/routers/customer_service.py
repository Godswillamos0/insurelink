from typing import Annotated
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect, UploadFile, File
from fastapi.responses import HTMLResponse
import io
import os
from pathlib import Path
#from pydub import AudioSegment
import asyncio
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from models import Users, InsuranceProduct, Premium, Claims
from database import SessionLocal
#from ai import run_model
from datetime import datetime
from .auth import get_current_user
from .ai_model import chat, transcribe

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


@router.post("/voice", status_code=status.HTTP_200_OK)
async def upload_and_transcribe(
        user: user_dependency,
        db: db_dependency,
        audio: Annotated[UploadFile, File(...)]
):  
    
    user_model = db.query(Users).filter(Users.id==user.get('id')).first()
    
    if audio.content_type not in ("audio/mpeg", "audio/wav", "audio/mp3", "audio/ogg"):
        raise HTTPException(status_code=400, detail="Invalid file type")

    contents = await audio.read()
    try:

        import io
        buffer = io.BytesIO(contents)
        transcript = transcribe(buffer)  # Adjust this line based on your transcription function
        await audio.close()  # Close the file after reading
        
        try:
            #response = chat(transcript)
            #now convert it to audio
            return chat(transcript)
        
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {e}")
 


@router.post("/tel_bot", status_code=status.HTTP_200_OK)
async def tel_bot_chat(request: PromptRequest):
    result = chat(request.message)
    return {"response": result}
   
    
    

