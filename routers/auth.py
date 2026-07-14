from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import User
from auth import create_access_token, verify_password
from fastapi.security import OAuth2PasswordRequestForm
from database import get_db

router = APIRouter()


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
     
    db_user = db.query(User).filter(User.username == form_data.username).first()
    
    if db_user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": form_data.username})
    return {"access_token":token, "token_type":"bearer"}
    