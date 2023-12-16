from fastapi import APIRouter, Response, HTTPException, status
from app.api.schemas.auth_mdoel import SAuth
from app.db.user_dao import UserDAO
from app.core.security import create_token_access 
from app.core.security import get_hashed_password
from exception import UserAlreadyExists


router = APIRouter(
    prefix="/auth", 
    tags=["AUTH"]
)


@router.post("/register")
async def reg_user(data: SAuth): 
    user = await UserDAO.get_user(username=data.username) 
    if user: 
        raise UserAlreadyExists
    
    hashed_password = get_hashed_password(data.password)
    await UserDAO.add_user(data.username, hashed_password)
    return {"message": "New user was added!"}


@router.post("/login") 
async def log_user(response: Response, data: SAuth):
    user = await UserDAO.get_user(username=data.username)
    if not user: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = create_token_access({"sub": str(user.username)})
    response.set_cookie("stepikxd", access_token, httponly=True)
    return {"access_token": access_token} 