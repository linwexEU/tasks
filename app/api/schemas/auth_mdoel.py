from pydantic import BaseModel 

class SAuth(BaseModel): 
    username: str 
    password: str
