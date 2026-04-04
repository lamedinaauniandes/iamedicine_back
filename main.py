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
from core.config import settings_urls

# def create_tables():
#     BASE.metadata.create_all(bind=engine)

# try:    
#     create_tables()
# except Exception as e: 
#     print(e)


load_dotenv(override=True)

logger = logging.getLogger("uvicorn.error")

app = FastAPI()

app.include_router(user.router)
app.include_router(chat.router)
app.include_router(auth.router)

def get_allowed_origins() -> List[str]:
    return [
        settings_urls.LOCAL_PORT3000,
        settings_urls.LOCAL2_PORT3000,
        settings_urls.IP_SERVER_PORT,
        settings_urls.IP_SERVER,
        ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"message":"hola mundo api-fast backend"}

if __name__=="__main__":
    uvicorn.run("main:app",port=8000,reload=True)
