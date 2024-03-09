from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class TranslationBase(BaseModel):
    language: str
    title: str
    description: str
    translated_text: str


class TranslationCreate(TranslationBase):
    pass


class TranslationUpdate(BaseModel):
    language: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    translated_text: Optional[str] = None


class Translation(TranslationBase):
    id: int
    article_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TranslationOut(Translation):
    pass
