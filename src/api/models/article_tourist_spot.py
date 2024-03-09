from sqlalchemy import Column, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship
from db import Base


class ArticleTouristSpot(Base):
    __tablename__ = "article_tourist_spots"

    article_id = Column(Integer, ForeignKey("articles.id"), primary_key=True)
    tourist_spot_id = Column(Integer, ForeignKey("tourist_spots.id"), primary_key=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    # articles = relationship("Article", back_populates="tourist_spots")
    # tourist_spots = relationship("TouristSpot", back_populates="articles")
