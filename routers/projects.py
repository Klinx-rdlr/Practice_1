from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Project
from schemas import ProjectCreate, ProjectResponse
from auth import get_current_user
from models import User

router = APIRouter()


@router.post("/projects", response_model=ProjectResponse)
def create_project(project: ProjectCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_project = Project(user_id=current_user.id, name=project.name, description=project.description)

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project

@router.get("/projects", response_model=list[ProjectResponse])
def list_projects(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    projects = db.query(Project).filter(Project.user_id == current_user.id).all()
    
    return projects

@router.put("/projects/{id}", response_model=ProjectResponse)
def update_project(id: int, project: ProjectCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    db_project = db.query(Project).filter(Project.id == id).first()
    
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if db_project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You have no access")
    
    db_project.name = project.name
    db_project.description = project.description

    db.commit()
    db.refresh(db_project)

    return db_project

@router.delete("/projects/{id}")
def delete_project(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_project = db.query(Project).filter(Project.id == id).first()

    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    if db_project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this project")

    db.delete(db_project)
    db.commit()

    return {"detail": "Project deleted"}