from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")


class Hash(): 

    def hash_password(password): 
        return pwd_context.hash(password)
    
    def verify_password(password_hash,password_body): 
        return pwd_context.verify(password_body,password_hash)