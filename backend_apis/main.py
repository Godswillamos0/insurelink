from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import customer_service, auth, admin, users, insurance
from routers.telegram_bot import start_telegram_bot
from typing import Annotated
import models
from routers import auth, admin, users, insurance
from database import engine
import asyncio


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


models.Base.metadata.create_all(bind=engine)

app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(insurance.router)
app.include_router(users.router)
app.include_router(customer_service.router)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_telegram_bot())



@app.get("/ping")
async def ping():
    return {"status": "alive"}
