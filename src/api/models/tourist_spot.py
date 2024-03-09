from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from sqlalchemy.orm import relationship
from db import Base


class TouristSpot(Base):
    __tablename__ = "tourist_spots"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    location = Column(String)
    description = Column(Text)
    average_stay_time = Column(Float)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    articles = relationship(
        "Article",
        secondary="article_tourist_spots",  # 中間テーブルの名前を指定
        back_populates="tourist_spots",
    )
