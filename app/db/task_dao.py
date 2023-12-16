from sqlalchemy import select, delete, update, insert

from app.db.database import async_session_maker 
from app.db.models import Tasks, TestTasks 

from config import settings


class TasksDAO: 
    model = Tasks if settings.MODE == "DEV" else TestTasks


    @classmethod
    async def get_task_by_data(cls, **filter_data): 
        async with async_session_maker() as session: 
            query = select("*").select_from(cls.model).filter_by(**filter_data)
            result = await session.execute(query) 
            return result.mappings().one_or_none() 
        

    @classmethod 
    async def get_tasks(cls): 
        async with async_session_maker() as session: 
            query = select("*").select_from(cls.model)
            result = await session.execute(query) 
            return result.mappings().all() 
        

    @classmethod 
    async def add_task(cls, name_user, name, state): 
        async with async_session_maker() as session: 
            query = insert(cls.model).values(
                name_user=name_user, name=name, state=state
            )
            await session.execute(query) 
            await session.commit()


    @classmethod 
    async def delete_task(cls, **filter_data): 
        async with async_session_maker() as session: 
            query = delete(cls.model).filter_by(**filter_data) 
            await session.execute(query) 
            await session.commit() 


    @classmethod 
    async def update_task(cls, name, state): 
        async with async_session_maker() as session: 
            query = update(cls.model).where(cls.model.name == name).values(state=state)
            await session.execute(query) 
            await session.commit()