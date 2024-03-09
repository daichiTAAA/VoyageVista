from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: str


class UserCreate(UserBase):
    hashed_password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    hashed_password: Optional[str] = None
    role: Optional[str] = None


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    created_at: datetime
    updated_at: datetime
    articles: List["ArticleOut"] = []
    feedbacks: List["FeedbackOut"] = []

    class Config:
        from_attributes = True


from .article import ArticleOut
from .feedback import FeedbackOut

UserOut.model_rebuild()


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
