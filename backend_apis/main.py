from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routers import customer_service, auth, admin, users, insurance
from routers.telegram_bot import telegram_app, configure_webhook
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



@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    await telegram_app.update_queue.put(data)
    return {"ok": True}



@app.on_event("startup")
async def startup_event():
    await configure_webhook()


@app.get("/ping")
async def ping():
    return {"status": "alive"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port="8000")
