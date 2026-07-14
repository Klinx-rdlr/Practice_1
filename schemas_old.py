from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    completed: bool = False
    user_id: int

class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool
    user_id: int

    model_config = {"from_attributes": True}
    

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str    

    model_config = {"from_attributes": True}
