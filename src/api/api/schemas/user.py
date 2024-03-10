from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[str] = None


class User(UserBase):
    id: int
    hashed_password: str
    created_at: datetime
    updated_at: datetime

    class ConfigDict:
        from_attributes = True


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    hashed_password: str
    created_at: datetime
    updated_at: datetime
    articles: List["ArticleOut"] = []
    feedbacks: List["FeedbackOut"] = []

    class ConfigDict:
        from_attributes = True


from .article import ArticleOut
from .feedback import FeedbackOut

UserOut.model_rebuild()


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
