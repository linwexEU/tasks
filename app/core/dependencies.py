from fastapi import Request, HTTPException, Depends, status 
from jose import JWTError, jwt
from app.db.user_dao import UserDAO 
from config import settings 
from datetime import datetime 


def get_token(request: Request): 
    token = request.cookies.get("stepikxd")
    if not token: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED) 
    return token 


async def get_current_user(token: str = Depends(get_token)): 
    try: 
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITH
        )
    except JWTError: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED) 
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()): 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED) 
    username = payload.get("sub")
    if not username: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED) 
    user = await UserDAO.get_user(username=username)
    if not user: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED) 
    
    return user











