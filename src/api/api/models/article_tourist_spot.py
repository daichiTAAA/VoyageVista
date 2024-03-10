from sqlalchemy import Column, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship
from api.db import Base


class ArticleTouristSpot(Base):
    __tablename__ = "article_tourist_spots"

    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("articles.id"))
    tourist_spot_id = Column(Integer, ForeignKey("tourist_spots.id"))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
