from jose import JWTError,jwt
from datetime import datetime,timedelta
from app.schemas import TokenData
from core.config import settings_hash

SECRET_KEY =  settings_hash.HASH_SECRET_KEY
ALGORITHM = settings_hash.HASH_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = 4320

def create_access_token(data:dict): 
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token:str,credentials_exception): 
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None: 
            raise credentials_exception
        token_data = TokenData(username=username)
        return token_data
    except JWTError:
        raise credentials_exception