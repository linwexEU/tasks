from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine 
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import settings


if settings.MODE == "DEV":  
    DATABASE_PARAMS = {} 
else: 
    DATABASE_PARAMS = {"poolclass": NullPool}


engine = create_async_engine(settings.DATABASE_URL, **DATABASE_PARAMS)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False) 

class Base(DeclarativeBase): 
    pass 






