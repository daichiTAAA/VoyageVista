from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class CulturalInsightBase(BaseModel):
    content: str


class CulturalInsightCreate(CulturalInsightBase):
    pass


class CulturalInsightUpdate(BaseModel):
    content: Optional[str] = None


class CulturalInsight(CulturalInsightBase):
    id: int
    created_at: datetime
    updated_at: datetime
    article_id: int

    class ConfigDict:
        from_attributes = True


class CulturalInsightOut(CulturalInsight):
    pass
