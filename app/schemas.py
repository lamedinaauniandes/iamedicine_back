from pydantic import BaseModel, Field
from typing import Optional,Union
from datetime import datetime

class User(BaseModel):
    nombre:str
    username:str
    password:str
    apellido:str
    direccion: Optional[str]
    telefono:int
    correo:str 
    tipo: int
    creacion:datetime = datetime.now()
    estado:bool = False

class UpdateUser(BaseModel):
    nombre:str=None
    username:str=None
    password:str=None
    apellido:str=None
    direccion:str=None
    telefono:int=None
    correo:str=None 
    tipo:int=None
    estado:bool=None

class UserId(BaseModel):
    id:int


class ShowUser(BaseModel): 
    username:str
    nombre:str
    correo:str
    class Config():
        orm_mode=True

class Login(BaseModel): 
    username:str
    password:str


class ChatRequest(BaseModel): 
    message: str = Field(...,min_length=1)

class ChatResponse(BaseModel): 
    reply: str

class Token(BaseModel): 
    acces_token:str
    token_type:str 


class TokenData(BaseModel): 
    username: Union[str,None] = None