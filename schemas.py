from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    completed: bool = False
    project_id: int

class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool
    project_id: int

    model_config = {"from_attributes": True}
    
class ProjectCreate(BaseModel):
    name: str
    description: str | None = None

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    user_id: int

    model_config = {"from_attributes": True}

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str    

    model_config = {"from_attributes": True}
