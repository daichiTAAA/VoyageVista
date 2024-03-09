from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class ArticleBase(BaseModel):
    title: str
    content: str
    status: str


class ArticleCreate(ArticleBase):
    author_id: int
    created_at: datetime
    updated_at: datetime


class ArticleUpdate(ArticleBase):
    title: Optional[str] = None
    content: Optional[str] = None
    status: Optional[str] = None


class Article(ArticleBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ArticleOut(BaseModel):
    id: int
    title: str
    content: str
    status: str
    author_id: int
    created_at: datetime
    updated_at: datetime
    photos: List["PhotoOut"] = []
    translations: List["TranslationOut"] = []
    tourist_spots: List["TouristSpotOut"] = []
    restaurants: List["RestaurantOut"] = []
    feedbacks: List["FeedbackOut"] = []
    cultural_insights: List["CulturalInsightOut"] = []

    class Config:
        from_attributes = True


from .photo import PhotoOut
from .translation import TranslationOut
from .tourist_spot import TouristSpotOut
from .restaurant import RestaurantOut
from .feedback import FeedbackOut
from .cultural_insight import CulturalInsightOut

ArticleOut.model_rebuild()
