### V2
import logging
from typing import List
from fastapi import (
    FastAPI, 
    HTTPException,
    )
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.routers import user,chat,auth
from app.db.database import BASE,engine


def create_tables():
    BASE.metadata.create_all(bind=engine)

try:    
    create_tables()
except Exception as e: 
    print(e)


load_dotenv(override=True)

logger = logging.getLogger("uvicorn.error")

app = FastAPI()

app.include_router(user.router,prefix="/users",tags=["User"])
app.include_router(chat.router,prefix="/chat",tags=["Chat"])
app.include_router(auth.router)


def get_allowed_origins() -> List[str]:
    # Dev default; en prod léelo de env
    return [
        "http://127.0.0.1:3000", 
        "http://localhost:3000",
        "http://52.202.191.134:3000",
        "http://52.202.191.134"
        ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"message":"hola mundo api-fast backend"}



if __name__=="__main__":
    uvicorn.run("main:app",port=8000,reload=True)
