from fastapi import Depends, Request, APIRouter, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from app.api.schemas.user_model import User
from app.api.schemas.task import Task
from app.core.dependencies import get_current_user 
from app.core.websockets import ConnectionManager

from app.db.task_dao import TasksDAO
from exception import TaskAlreadyExists, TaskNotFound


router = APIRouter(
    prefix="/tasks", 
    tags=["TASKS"]
)

manager = ConnectionManager()

templates = Jinja2Templates(directory="app/templates")


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket): 
    await manager.connect(websocket) 
     
    await websocket.accept()
    
    try: 
        while True: 
            data = await websocket.receive_text() 
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect: 
        manager.disconnect(websocket) 


@router.get("/get_all_tasks")
async def get_all_tasks(request: Request, current_user: User = Depends(get_current_user)): 
    tasks = await TasksDAO.get_tasks() 
    return templates.TemplateResponse(name="index.html", context={"request": request, "tasks": tasks})


@router.post("/add_task")
async def add_task_to_db(data_task: Task, current_user: User = Depends(get_current_user)): 
    tasks = await TasksDAO.get_task_by_data(name=data_task.name)
    if tasks: 
        raise TaskAlreadyExists
    
    await TasksDAO.add_task(
        name_user=current_user.username, name=data_task.name, state=data_task.state
    )

    await manager.send_message(
        {"event": "websocket_task", "msg": f"{current_user.username} add task. Update the page to see the change."}
    )

    return {"message": "Success!"} 


@router.delete("/delete_task") 
async def delete_task_from_db(
    name: str | None = None, 
    state: str | None = None, 
    current_user: User = Depends(get_current_user)
): 
    if name: 
        await TasksDAO.delete_task(name=name)
    if state: 
        await TasksDAO.delete_task(state=state) 
    if name and state: 
        await TasksDAO.delete_task(name_user=current_user.username, name=name, state=state) 
    if (not name) and (not state): 
        await TasksDAO.delete_task(name_user=current_user.username)

    await manager.send_message(
        {"event": "websocket_task", "msg": f"{current_user.username} delete task. Update the page to see the change."}
    )

    return {"message": "Success!"}


@router.put("/update_task")
async def update_exist_task(data_task: Task, current_user: User = Depends(get_current_user)): 
    task = await TasksDAO.get_task_by_data(name=data_task.name) 
    if not task: 
        raise TaskNotFound
    
    await TasksDAO.update_task(data_task.name, data_task.state)

    await manager.send_message(
        {"event": "websocket_task", "msg": f"{current_user.username} ({data_task.name}) change state to '{data_task.state}'. Update the page to see the change."}
    )

    return {"message": "Success!"}






