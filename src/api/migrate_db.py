from sqlalchemy import create_engine

from db import Base, db_engine

# モデルクラスをインポート
from models.user import User
from models.article import Article
from models.article_restaurant import ArticleRestaurant
from models.article_tourist_spot import ArticleTouristSpot
from models.photo import Photo
from models.translation import Translation
from models.tourist_spot import TouristSpot
from models.restaurant import Restaurant
from models.feedback import Feedback
from models.cultural_insight import CulturalInsight


def reset_database():
    Base.metadata.drop_all(bind=db_engine)
    Base.metadata.create_all(bind=db_engine)


def create_database():
    Base.metadata.create_all(bind=db_engine)


if __name__ == "__main__":
    create_database()
