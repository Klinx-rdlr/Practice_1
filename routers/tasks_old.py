from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from database import get_db
from schemas import TaskCreate, TaskResponse
from models import Task, User

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "healthy"}


@router.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(**task.model_dump())

    user = db.query(User).filter(User.id == task.user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.get("/tasks", response_model=list[TaskResponse])
def list_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks


@router.get("/tasks/{id}", response_model=TaskResponse)
def get_task(id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/tasks/{id}")
def delete_task(id: int, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == id).first()

    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(db_task)
    db.commit()

    return {"detail":"Task Deleted"}

@router.put("/tasks/{id}", response_model=TaskResponse)
def update_task(id: int, updated_task: TaskCreate, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == id).first()

    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db_task.title = updated_task.title

    db.commit()
    db.refresh(db_task)

    return db_task