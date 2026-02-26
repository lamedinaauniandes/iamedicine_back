from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from app.token import verify_token

oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token:str=Depends(oauth_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="credenciales no validas", 
        headers ={"WWW-Authenticate":"Bearer"}, 
    )
    return verify_token(token,credentials_exception)
