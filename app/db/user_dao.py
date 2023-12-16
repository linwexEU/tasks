from sqlalchemy import insert, select 
from app.db.database import async_session_maker 

from app.db.models import Users, TestUsers

from config import settings


class UserDAO: 
    model = Users if settings.MODE == "DEV" else TestUsers

    @classmethod 
    async def add_user(cls, username, hashed_password): 
        async with async_session_maker() as session: 
            query = insert(cls.model).values(username=username, hashed_password=hashed_password) 
            await session.execute(query)
            await session.commit() 


    @classmethod 
    async def get_user(cls, **filter_data): 
        async with async_session_maker() as session: 
            query = select("*").select_from(cls.model).filter_by(**filter_data) 
            result = await session.execute(query) 
            return result.mappings().one_or_none() 
    
