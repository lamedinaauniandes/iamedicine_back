from sqlalchemy.orm import Session
from app import schemas
from app.db import models
from fastapi import status,HTTPException
from passlib.context import CryptContext

class Usuario: 

    def __init__(self,db:Session): 
        self.db = db
        self.pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
    
    def crear(self,usuario:schemas.User):
      
        try: 
            pass_hash = self.pwd_context.hash(usuario.password)
            usuario = usuario.dict()
            nuevo_usuario = models.User(
                nombre = usuario["nombre"],
                username = usuario["username"],
                password = pass_hash,
                apellido = usuario["apellido"],
                direccion = usuario["direccion"],
                telefono = usuario["telefono"],
                correo = usuario["correo"],
                tipo = usuario["tipo"],
                # creacion = usuario["creacion"],
                # estado = usuario["estado"],
            )
            self.db.add(nuevo_usuario)
            self.db.commit()
            self.db.refresh(nuevo_usuario)
        except Exception as e: 
            raise HTTPException(
                detail=f" {e}",
                status_code=status.HTTP_409_CONFLICT
            )

        return {"respuesta":"Usuario creado correctamente!"}
    
    def obtener_usuarios(self):
        data = self.db.query(models.User).all()
        return data
    
    def obtener_usuario(self,user_id:int): 
        usuario = self.db.query(models.User).filter(models.User.id == user_id).first()
        if not usuario: 
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail= f" {e}"
            )
        return usuario
    
    def eleminar_usuario(self,user_id:int): 
        usuario = self.db.query(models.User).filter(models.User.id == user_id)
        if not usuario.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{e}"
            )
        
        usuario.delete(synchronize_session=False)
        self.db.commit() 
        return {"respuesta":"usuario eliminado correctamente"}
    
    def actualizar_usuario(self,user_id:int,updateUser:schemas.UpdateUser): 
        usuario = self.db.query(models.User).filter(models.User.id == user_id)
        
        if not usuario.first(): 
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail= f" {e}"
            )
        
        usuario.update(updateUser.dict( exclude_unset = True ))
        self.db.commit()
        return {"respuesta":"usuario actualizado correctamente"}
