from datetime import datetime, timedelta 
from passlib.context import CryptContext 
from jose import jwt 
from config import settings 

from app.db.user_dao import UserDAO


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str): 
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str): 
    return pwd_context.verify(plain_password, hashed_password) 


def create_token_access(data: dict): 
    to_encode = data.copy() 
    expire = datetime.utcnow() + timedelta(days=14) 
    to_encode.update({"exp": expire}) 
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, settings.ALGORITH
    )
    return encoded_jwt


async def authenticate_user(username, password): 
    user = await UserDAO.get_user(username=username)
    if user and verify_password(password, user.hashed_password): 
        return user 
    return None 



