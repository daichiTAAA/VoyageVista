from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from api.db import Base


class Translation(Base):
    __tablename__ = "translations"

    id = Column(Integer, primary_key=True, index=True)
    language = Column(String)
    title = Column(String)
    description = Column(Text)
    translated_text = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    article_id = Column(Integer, ForeignKey("articles.id"))

    article = relationship("Article", back_populates="translations", lazy="joined")
