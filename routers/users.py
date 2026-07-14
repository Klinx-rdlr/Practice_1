from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from database import get_db
from schemas import UserCreate, UserResponse
from models import User
from auth import hash_password, verify_password, create_access_token

router = APIRouter()


@router.get("/users", response_model=list[UserResponse])
def list_user(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@router.get("/users/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    
    if user is None:
         raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password) 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

