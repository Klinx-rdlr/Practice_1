from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User

import bcrypt
import os
from dotenv import load_dotenv

from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
print(f">>> SECRET_KEY loaded: {SECRET_KEY is not None}, ALGORITHM: {ALGORITHM}")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
    )
    print(f">>> token received: {token[:20]}...")   # did a token even arrive?
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f">>> decoded payload: {payload}")     # did decode succeed?
        username = payload.get("sub")
        if username is None:
            print(">>> no sub in payload")
            raise credentials_exception
    except JWTError as e:
        print(f">>> JWTError: {e}")                   # the real decode error
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        print(f">>> no user found for username: {username}")
        raise credentials_exception
    return user

def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:

    plain = plain_password.encode("utf-8")
    hashed = hashed_password.encode("utf-8")

    return bcrypt.checkpw(plain, hashed)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt




