from datetime import datetime
import importlib

from dotenv import load_dotenv
from pydantic import BaseModel, EmailStr, Field, validator

import PostgresAndRedisManager

importlib.reload(PostgresAndRedisManager)

from PostgresAndRedisManager import (
    EnvInfo,
    PostgresAndRedisManager,
    PostgresConfig,
    RedisConfig,
    get_env_info,
)


class UserModel(BaseModel):
    """ユーザーのデータモデル"""

    id: int
    username: str = Field(..., min_length=1)
    email: EmailStr
    password: str = Field(..., min_length=6)


class ArticleModel(BaseModel):
    """記事のデータモデル"""

    id: int
    user_id: int
    title: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)
    created_at: datetime
    updated_at: datetime

    @validator("created_at", "updated_at")
    def validate_dates(cls, v):
        if v > datetime.now():
            raise ValueError("dates cannot be in the future.")
        return v


class DBManager:
    """PostgresAndRedisManagerを使用して、データベースを操作するためのクラス"""

    def __init__(self):
        load_dotenv(".env")
        self.env_info: EnvInfo = get_env_info(EnvInfo)
        self.postgres_config = PostgresConfig(
            PG_USER=self.env_info.PG_USER,
            PG_PASSWORD=self.env_info.PG_PASSWORD,
            PG_DATABASE=self.env_info.PG_DATABASE,
        )
        self.redis_config = RedisConfig(REDIS_PASSWORD=self.env_info.REDIS_PASSWORD)
        self.manager: PostgresAndRedisManager = self._initialize_manager()
        self._create_tables()

    def _initialize_manager(self) -> PostgresAndRedisManager:
        """PostgresAndRedisManagerのインスタンスを作成する関数"""
        manager = PostgresAndRedisManager(
            self.postgres_config,
            self.redis_config,
            allowed_tables=[
                "users",
                "articles",
                "photos",
                "translations",
                "touristspots",
                "restaurants",
                "articletouristspot",
                "articlerestaurant",
            ],
        )
        return manager

    def _create_tables(self):
        """テーブルを作成する関数"""
        # Define your SQL queries to create tables
        create_users_table = """
      CREATE TABLE IF NOT EXISTS users (
          id SERIAL PRIMARY KEY,
          username VARCHAR(255) NOT NULL,
          email VARCHAR(255) NOT NULL UNIQUE,
          password VARCHAR(255) NOT NULL
      );
      """
        create_articles_table = """
      CREATE TABLE IF NOT EXISTS articles (
          id SERIAL PRIMARY KEY,
          user_id INTEGER NOT NULL REFERENCES users(id),
          title VARCHAR(255) NOT NULL,
          content TEXT NOT NULL,
          created_at TIMESTAMP NOT NULL,
          updated_at TIMESTAMP NOT NULL
      );
      """

        create_photos_table = """
      CREATE TABLE IF NOT EXISTS photos (
          id SERIAL PRIMARY KEY,
          article_id INTEGER NOT NULL REFERENCES articles(id),
          file_path VARCHAR(255) NOT NULL,
          description TEXT,
          created_at TIMESTAMP NOT NULL
      );
      """

        create_translations_table = """
      CREATE TABLE IF NOT EXISTS translations (
          id SERIAL PRIMARY KEY,
          article_id INTEGER NOT NULL REFERENCES articles(id),
          language VARCHAR(50) NOT NULL,
          translated_text TEXT NOT NULL
      );
      """

        create_touristspots_table = """
      CREATE TABLE IF NOT EXISTS touristspots (
          id SERIAL PRIMARY KEY,
          name VARCHAR(255) NOT NULL,
          location VARCHAR(255) NOT NULL,
          description TEXT,
          average_stay_time FLOAT
      );
      """

        create_restaurants_table = """
      CREATE TABLE IF NOT EXISTS restaurants (
          id SERIAL PRIMARY KEY,
          name VARCHAR(255) NOT NULL,
          location VARCHAR(255) NOT NULL,
          cuisine VARCHAR(255),
          link_to_external_review TEXT
      );
      """

        create_article_touristspot_table = """
      CREATE TABLE IF NOT EXISTS articletouristspot (
          article_id INTEGER NOT NULL REFERENCES articles(id),
          tourist_spot_id INTEGER NOT NULL REFERENCES touristspots(id),
          PRIMARY KEY (article_id, tourist_spot_id)
      );
      """

        create_article_restaurant_table = """
      CREATE TABLE IF NOT EXISTS articlerestaurant (
          article_id INTEGER NOT NULL REFERENCES articles(id),
          restaurant_id INTEGER NOT NULL REFERENCES restaurants(id),
          PRIMARY KEY (article_id, restaurant_id)
      );
      """

        # Execute the queries to create tables
        for create_table_query in [
            create_users_table,
            create_articles_table,
            create_photos_table,
            create_translations_table,
            create_touristspots_table,
            create_restaurants_table,
            create_article_touristspot_table,
            create_article_restaurant_table,
        ]:
            self.manager.query(create_table_query)

    def get_table_names(self):
        """テーブルの一覧を取得する関数"""
        key = f"table_names"
        # テーブルの一覧を取得するクエリを実行
        query_get_tables = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
        # テーブル名のリストを取得
        tables = self.manager.get_data(key, query_get_tables)
        # 取得したテーブル名を出力
        print("テーブルの一覧:")
        for table in tables:
            print(table[0])

    def get_table_info(self, table_name: str):
        """テーブルのメタ情報を取得する関数"""
        # Redisキーの定義
        key = f"table_info_{table_name}"
        query_get_table_info = """
        SELECT column_name, data_type, character_maximum_length, column_default, is_nullable
        FROM information_schema.columns
        WHERE table_name = %s AND table_schema = 'public'
        ORDER BY ordinal_position;
        """
        # テーブル情報の取得
        table_info = self.manager.query(key, query_get_table_info, None, (table_name,))

        # 取得したテーブル情報を出力
        print(f"情報: {table_name} テーブル")
        for column in table_info:
            print(
                f"列名: {column[0]}, データ型: {column[1]}, 最大長: {column[2]}, デフォルト値: {column[3]}, NULL許容: {column[4]}"
            )

    def get_record_by_id(self, table_name: str, record_id: int):
        """指定されたテーブルからIDによってレコードを取得する関数"""
        key = f"record_{table_name}_{record_id}"
        # SQLインジェクションを防ぐため、テーブル名の検証が必要です
        if table_name not in self.manager.allowed_tables:
            raise ValueError(f"Invalid table name: {table_name}")

        query_get_record = f"""
        SELECT * FROM {table_name}
        WHERE id = %s;
        """
        # パラメータをタプルとして渡す
        params = (record_id,)

        record = self.manager.get_data(key, query_get_record, params=params)
        if record:
            print(f"Record in {table_name} with ID {record_id}: {record}")
            return record
        else:
            print(f"No record found in {table_name} with ID {record_id}")
            return None

    def add_user(self, user_data: UserModel):
        """ユーザーを追加する関数"""
        # パスワードハッシュ化（ここでは簡単な例として平文で保存）
        # 実際には安全なハッシュ関数を使用するべきです
        hashed_password = (
            user_data.password
        )  # この行はハッシュ化の例を示すためのものです

        insert_user_query = """
        INSERT INTO users (id, username, email, password)
        VALUES (%s, %s, %s, %s);
        """
        self.manager.query(
            insert_user_query,
            None,
            (
                user_data.id,
                user_data.username,
                user_data.email,
                hashed_password,
            ),
        )
        print("ユーザーが追加されました。")

    def add_article(self, article_data: ArticleModel):
        """記事を追加する関数"""
        insert_article_query = """
        INSERT INTO articles (id, user_id, title, content, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        self.manager.query(
            insert_article_query,
            None,
            (
                article_data.id,
                article_data.user_id,
                article_data.title,
                article_data.content,
                article_data.created_at,
                article_data.updated_at,
            ),
        )
        print("記事が追加されました。")


if __name__ == "__main__":
    # DBManagerのインスタンスを作成
    db_manager = DBManager()
    # テーブルの一覧を取得する
    # db_manager.get_table_names()

    # usersテーブルにユーザーを追加する
    user = UserModel(
        id=1, username="testuser", email="test@test.com", password="password"
    )
    # db_manager.add_user(user)
    # usersテーブルのメタ情報を取得する
    # db_manager.get_table_info("users")
    # usersテーブルからIDによってレコードを取得する
    db_manager.get_record_by_id("users", 1)

    # articlesテーブルに記事を追加する
    article = ArticleModel(
        id=1,
        user_id=1,
        title="サンプル記事",
        content="記事の内容",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    # db_manager.add_article(article)
    # articlesテーブルのメタ情報を取得する
    # db_manager.get_table_info("articles")
    # articlesテーブルからIDによってレコードを取得する
    db_manager.get_record_by_id("articles", 1)
