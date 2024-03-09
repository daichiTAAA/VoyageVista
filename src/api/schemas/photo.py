from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class PhotoBase(BaseModel):
    file_path: str
    description: Optional[str] = None


class PhotoCreate(PhotoBase):
    pass


class PhotoUpdate(BaseModel):
    file_path: Optional[str] = None
    description: Optional[str] = None


class Photo(PhotoBase):
    id: int
    article_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PhotoOut(Photo):
    pass
