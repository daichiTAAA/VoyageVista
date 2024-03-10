from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

import api.schemas as schemas
import api.cruds as cruds
from api.db import SessionLocal
from api.security.password import verify_password
from api.get_env import get_env_info


class EnvInfo(BaseModel):
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


env_info: EnvInfo = get_env_info(EnvInfo)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def authenticate_user(db: Session, username: str, password: str):
    # 修正: get_user_by_username -> get_user_by_email
    user = cruds.get_user_by_email(
        db, email=username
    )  # username は実際には email を表している
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=env_info.ACCESS_TOKEN_EXPIRE_MINUTES
        )  # 修正: ハードコーディングから変数を使用
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, env_info.SECRET_KEY, algorithm=env_info.ALGORITHM
    )
    return encoded_jwt


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, env_info.SECRET_KEY, algorithms=[env_info.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = cruds.get_user_by_email(
        db, email=token_data.username
    )  # username は実際には email を表している
    if user is None:
        raise credentials_exception
    return user
