from datetime import datetime
from pydantic import BaseModel


class ArticleTouristSpotBase(BaseModel):
    article_id: int
    tourist_spot_id: int


class ArticleTouristSpotCreate(ArticleTouristSpotBase):
    pass


class ArticleTouristSpotUpdate(ArticleTouristSpotBase):
    pass


class ArticleTouristSpotInDBBase(ArticleTouristSpotBase):
    created_at: datetime
    updated_at: datetime

    class ConfigDict:
        from_attributes = True


class ArticleTouristSpot(ArticleTouristSpotInDBBase):
    pass
