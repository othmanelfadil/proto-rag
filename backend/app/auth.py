from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from .database import get_db
from .models import User
import jwt

#change to another token when in production
#make the secret key an environment variable
# or use a secret management service
# for production
SECRET_KEY = "supersecretkeythatshouldnotbehardcoded"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# hash password 
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta=None):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
     try:
         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
         username: str = payload.get("sub")
         if username is None:
             raise HTTPException(status_code=401, detail="Invalid authentication credentials")
         user = db.query(User).filter(User.username == username).first()
         if user is None:
             raise HTTPException(status_code=401, detail="User not found")
         return user
     except:
         raise HTTPException(status_code=401, detail="Invalid authentication credentials")


