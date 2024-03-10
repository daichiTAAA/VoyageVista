from sqlalchemy import Column, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship
from db import Base


class ArticleRestaurant(Base):
    __tablename__ = "article_restaurants"

    article_id = Column(Integer, ForeignKey("articles.id"), primary_key=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), primary_key=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
