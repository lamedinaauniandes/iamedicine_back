from fastapi import APIRouter,Depends,status 
from fastapi.security import OAuth2PasswordRequestForm
from app.db.database import get_db
from sqlalchemy.orm import Session
from typing import List
from app.schemas import Login
from app.repository.auth import auth_user


router = APIRouter(
    prefix='/login',
    tags=['Login']
)

@router.post("/",status_code=status.HTTP_200_OK)
def login(login:OAuth2PasswordRequestForm=Depends(),db:Session = Depends(get_db)):
    auth_token = auth_user(usuario=login,db=db)
    return auth_token
