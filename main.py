from fastapi import FastAPI 
from app.api.endpoints.users import router as router_auth 
from app.api.endpoints.tasks import router as router_task

app = FastAPI() 

app.include_router(router_auth)
app.include_router(router_task)
