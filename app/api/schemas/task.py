from pydantic import BaseModel 


class Task(BaseModel): 
    name: str 
    state: str

