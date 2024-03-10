from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class FeedbackBase(BaseModel):
    content: str


class FeedbackCreate(FeedbackBase):
    pass


class FeedbackUpdate(BaseModel):
    content: Optional[str] = None


class Feedback(FeedbackBase):
    id: int
    user_id: int
    article_id: int
    created_at: datetime
    updated_at: datetime

    class ConfigDict:
        from_attributes = True


class FeedbackOut(Feedback):
    pass
