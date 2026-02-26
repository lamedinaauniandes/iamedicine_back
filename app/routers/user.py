from fastapi import APIRouter,Depends,status
from app.schemas import User, ShowUser, UpdateUser
from app.db.database import get_db
from sqlalchemy.orm import Session 
from app.db import models
from typing import List
from ..repository.user import Usuario 
from app.oauth import get_current_user

router = APIRouter()
 

@router.post("/",status_code=status.HTTP_201_CREATED)
def crear_usuario(user:User,db:Session = Depends(get_db),current_user:User=Depends(get_current_user)): 
    usuario = Usuario(db)
    res = usuario.crear(user)
    return res

@router.get("/",response_model=List[ShowUser],status_code=status.HTTP_200_OK)
def obtener_usuarios( db:Session = Depends(get_db),current_user: User=Depends(get_current_user)):
    usuario = Usuario(db)
    res = usuario.obtener_usuarios()
    return res

@router.get("/{user_id}",response_model=ShowUser,status_code=status.HTTP_200_OK)
def obtener_usuario(user_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    usuario = Usuario(db)
    res = usuario.obtener_usuario(user_id)
    return res

@router.delete('/',status_code=status.HTTP_200_OK)
def eliminar_usuario(user_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    usuario = Usuario(db)
    res = usuario.eleminar_usuario(user_id)
    return res

@router.patch('/{user_id}',status_code=status.HTTP_200_OK)
def actualizar_user(user_id:int,updateUser:UpdateUser,db:Session = Depends(get_db),current_user:User=Depends(get_current_user)):
    usuario = Usuario(db)
    res = usuario.actualizar_usuario(user_id,updateUser)
    return res
            
@router.post("/prueba",response_model=List[ShowUser],status_code=status.HTTP_200_OK)
def obtener_usuarios_hide2( db:Session = Depends(get_db)):
    usuario = Usuario(db)
    res = usuario.obtener_usuarios()
    return res

@router.post("/hide",status_code=status.HTTP_201_CREATED)
def crear_usuario_hide(user:User,db:Session = Depends(get_db)):
    usuario = Usuario(db)
    res = usuario.crear(user)
    return res



