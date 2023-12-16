from sqlalchemy import Column, String, Integer
from app.db.database import Base 


class Users(Base): 
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False) 
    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)


class Tasks(Base): 
    __tablename__ = "tasks" 

    id = Column(Integer, primary_key=True, nullable=False) 
    name_user = Column(String, nullable=False)
    name = Column(String, nullable=False) 
    state = Column(String, nullable=False)


class TestUsers(Base): 
    __tablename__ = "test_users"

    id = Column(Integer, primary_key=True, nullable=False) 
    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)


class TestTasks(Base): 
    __tablename__ = "test_tasks" 

    id = Column(Integer, primary_key=True, nullable=False) 
    name_user = Column(String, nullable=False)
    name = Column(String, nullable=False) 
    state = Column(String, nullable=False)
