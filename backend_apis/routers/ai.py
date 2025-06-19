from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from models import Users
from database import SessionLocal
#from ai import run_model
from datetime import datetime
from .auth import get_current_user

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
    
    
@router.post("/ask", status_code=status.HTTP_200_OK)
async def ai_response(user: user_dependency,
                      db: db_dependency, 
                      message: PromptRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    user_id = user.get("id")
    
    # Get chat history from DB
    chat_history = get_chat_history(user_id, db)

    # Run the model with user's message and history
    ai_reply = run_model(user_prompt=message.message, chat_history=chat_history)

    # Save the message and response to the database
    message_model = Messages(
        user_prompt=message.message,
        therapist_response=ai_reply,
        owner_id=user_id,
        time=datetime.now()
    )
    db.add(message_model)
    db.commit()

    return {"response": ai_reply}



def get_chat_history(user_id: int, db: Session):
    messages = (
        db.query(Messages)
        .filter(Messages.owner_id == user_id)
        .order_by(Messages.time.asc())
        .limit(10)
        .all()
    )

    history = ""
    for msg in messages:
        history += f"User: {msg.user_prompt}\nTherapist: {msg.therapist_response}\n"
    
    return history.strip()


@router.post("/personalised_options", status_code=status.HTTP_200_OK)
async def ai_response(user: user_dependency,
                      db: db_dependency, 
                      message: PromptRequest):
    pass