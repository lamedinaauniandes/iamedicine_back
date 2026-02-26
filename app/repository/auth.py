from sqlalchemy.orm import Session
from app.db import models
from fastapi import HTTPException,status
from app.schemas import Login
from app.hashing import Hash
from app.token import create_access_token

def auth_user(usuario:Login,db:Session):
    user = db.query(models.User).filter(models.User.username==usuario.username).first()
    if not user: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"no se encuentra User"
        )
    if not Hash.verify_password(user.password, usuario.password ):
        print("entramos a la excepción del logeo, no coincide el password")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="No autorizado"
        )
    
    access_token = create_access_token(
        data={"sub":user.username}
    )
    return {"access_token":access_token,"token_type":"bearer"}
    