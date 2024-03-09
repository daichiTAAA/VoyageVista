from sqlalchemy import Column, ForeignKey, Integer, Text, DateTime
from sqlalchemy.orm import relationship
from db import Base


class CulturalInsight(Base):
    __tablename__ = "cultural_insights"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    article_id = Column(Integer, ForeignKey("articles.id"))

    article = relationship("Article", back_populates="cultural_insights")
