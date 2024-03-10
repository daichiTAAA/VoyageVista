from sqlalchemy import create_engine

from api.db import Base, db_engine_sync

# モデルクラスをインポート
from api.models.user import User
from api.models.article import Article
from api.models.article_restaurant import ArticleRestaurant
from api.models.article_tourist_spot import ArticleTouristSpot
from api.models.photo import Photo
from api.models.translation import Translation
from api.models.tourist_spot import TouristSpot
from api.models.restaurant import Restaurant
from api.models.feedback import Feedback
from api.models.cultural_insight import CulturalInsight


def reset_database():
    Base.metadata.drop_all(bind=db_engine_sync)
    Base.metadata.create_all(bind=db_engine_sync)


def create_database():
    Base.metadata.create_all(bind=db_engine_sync)


if __name__ == "__main__":
    reset_database()
