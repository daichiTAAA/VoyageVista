from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from api.db import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    location = Column(String)
    cuisine = Column(String)
    link_to_external_review = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    articles = relationship(
        "Article",
        secondary="article_restaurants",  # 中間テーブルの名前を指定
        back_populates="restaurants",
    )
