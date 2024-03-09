from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    DateTime,
    Float,
)
from sqlalchemy.orm import relationship
from db import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    status = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    author_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User", back_populates="articles")
    photos = relationship("Photo", back_populates="article")
    translations = relationship("Translation", back_populates="article")
    tourist_spots = relationship(
        "TouristSpot",
        secondary="article_tourist_spots",  # 中間テーブルの名前を指定
        back_populates="articles",
    )
    restaurants = relationship(
        "Restaurant",
        secondary="article_restaurants",  # 中間テーブルの名前を指定
        back_populates="articles",
    )
    feedbacks = relationship("Feedback", back_populates="article")
    cultural_insights = relationship("CulturalInsight", back_populates="article")
