from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from database import get_db
from schemas import TaskCreate, TaskResponse
from models import Task, User
from auth import get_current_user

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "healthy"}


@router.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_task = Task(title=task.title, completed=task.completed, user_id=current_user.id)

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.get("/tasks", response_model=list[TaskResponse])
def list_tasks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    tasks = db.query(Task).filter(Task.user_id == current_user.id).all()
    return tasks


@router.get("/tasks/{id}", response_model=TaskResponse)
def get_task(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == id).first()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this task")
    
    return task


@router.delete("/tasks/{id}")
def delete_task(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_task = db.query(Task).filter(Task.id == id).first()

    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if db_task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this task")
    
    db.delete(db_task)
    db.commit()

    return {"detail":"Task Deleted"}

@router.put("/tasks/{id}", response_model=TaskResponse)
def update_task(id: int, updated_task: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_task = db.query(Task).filter(Task.id == id).first()

    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if db_task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this task")
    
    db_task.title = updated_task.title

    db.commit()
    db.refresh(db_task)

    return db_task