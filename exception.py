from fastapi import HTTPException, status


class AppException(HTTPException): 
    status_code = 500 
    detail = "" 

    def __init__(self): 
        super().__init__(status_code=self.status_code, detail=self.detail)


class TaskAlreadyExists(AppException): 
    status_code = status.HTTP_409_CONFLICT 
    detail = "Task already exists"


class TaskNotFound(AppException): 
    status_code = status.HTTP_404_NOT_FOUND 
    detail = "Task doesn't exists"


class UserAlreadyExists(AppException): 
    status_code = status.HTTP_409_CONFLICT 
    detail = "User aleready exists"





















