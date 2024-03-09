from datetime import datetime
from pydantic import BaseModel


class ArticleRestaurantBase(BaseModel):
    article_id: int
    restaurant_id: int


class ArticleRestaurantCreate(ArticleRestaurantBase):
    pass


class ArticleRestaurantUpdate(ArticleRestaurantBase):
    pass


class ArticleRestaurantInDBBase(ArticleRestaurantBase):
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ArticleRestaurant(ArticleRestaurantInDBBase):
    pass
