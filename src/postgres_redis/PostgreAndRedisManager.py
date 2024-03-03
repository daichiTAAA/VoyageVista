import os
from typing import Type, TypeVar

from dotenv import load_dotenv
import psycopg2
from pydantic import BaseModel, ValidationError, TypeAdapter
import redis


class EnvInfo(BaseModel):
    PG_VERSION: str
    PG_CONTAINER_NAME: str
    PG_HOST: str
    PG_USER: str
    PG_PASSWORD: str
    REDIS_PASSWORD: str


class PostgresConfig(BaseModel):
    PG_USER: str
    PG_PASSWORD: str
    PG_HOST: str = "localhost"
    PG_PORT: str = "5432"
    PG_DATABASE: str = "test_db"
    PG_TABLE: str = "test_table"


class RedisConfig(BaseModel):
    REDIS_PASSWORD: str
    REDIS_HOST: str = "localhost"
    REDIS_PORT: str = "6379"


T = TypeVar("T")


def create_instance_from_env(dataclass_type: Type[T]) -> T:
    field_info = dataclass_type.__annotations__

    init_values = {}
    for field_name, field_type in field_info.items():
        env_value = os.getenv(field_name.upper())  # 環境変数は大文字で取得
        if env_value is not None:
            try:
                # TypeAdapterを使用して型変換を試みる
                adapter = TypeAdapter(field_type)
                converted_value = adapter.validate_python(env_value)
            except ValidationError:
                # バリデーションエラーが発生した場合は、変換せずに元の値を使用
                converted_value = env_value
            init_values[field_name] = converted_value

    try:
        return dataclass_type(**init_values)
    except ValidationError as e:
        print(f"Validation error: {e}")
        raise


def get_env_info(env_info_class: Type[BaseModel]) -> BaseModel:
    """環境変数から設定を読み込んで、指定されたデータクラスのインスタンスを作成する

    Arguments:
    ----------
        env_info_class (Type[BaseModel]): 環境変数から読み込む設定のデータクラス

    Notes:
    ------
    使用例:
    ```python
    class EnvInfo(BaseModel):
        PG_VERSION: str
        PG_CONTAINER_NAME: str
        PG_HOST: str
        PG_USER: str
        PG_PASSWORD: str
        REDIS_PASSWORD: str

    env_info: EnvInfo = get_env_info(EnvInfo)
    PG_USER = env_info.PG_USER
    ```
    """
    # .envファイルを探して、あれば読み込む
    load_dotenv()
    env_info_instance: BaseModel = create_instance_from_env(env_info_class)
    return env_info_instance


class PostgreAndRedisManager:
    def __init__(
        self,
        postgresConfig: PostgresConfig,
        redisConfig: RedisConfig,
        allowed_tables: list[str] = [],
    ):
        self.postgresConfig = postgresConfig
        if self.check_database_exists() is False:
            self.create_new_database()
        self.redisConfig = redisConfig
        self.r = redis.Redis(
            host=self.redisConfig.REDIS_HOST,
            port=self.redisConfig.REDIS_PORT,
            password=self.redisConfig.REDIS_PASSWORD,
            decode_responses=True,
        )
        self.allowed_tables = allowed_tables
        self.allowed_tables.append(self.postgresConfig.PG_TABLE)

    def check_database_exists(self):
        with psycopg2.connect(
            dbname="postgres",
            user=self.postgresConfig.PG_USER,
            password=self.postgresConfig.PG_PASSWORD,
            host=self.postgresConfig.PG_HOST,
            port=self.postgresConfig.PG_PORT,
        ) as conn:
            with conn.cursor() as cur:
                # 指定したデータベースが存在するかどうかを確認するSQLクエリ
                query = "SELECT 1 FROM pg_database WHERE datname = %s;"
                params = (self.postgresConfig.PG_DATABASE,)
                cur.execute(query, params)
                # クエリの結果を取得
                exists = cur.fetchone() is not None
                if exists:
                    print(
                        f"データベース '{self.postgresConfig.PG_DATABASE}' は存在します。"
                    )
                    return True
                else:
                    print(
                        f"データベース '{self.postgresConfig.PG_DATABASE}' は存在しません。"
                    )
                    return False

    def create_new_database(self):
        # デフォルトデータベースに接続
        with psycopg2.connect(
            dbname="postgres",
            user=self.postgresConfig.PG_USER,
            password=self.postgresConfig.PG_PASSWORD,
            host=self.postgresConfig.PG_HOST,
            port=self.postgresConfig.PG_PORT,
        ) as conn:
            conn.autocommit = True
            # カーソルを作成
            with conn.cursor() as cur:
                # 新しいデータベースを作成（既に存在する場合は不要）
                query = "CREATE DATABASE %s;"
                params = (self.postgresConfig.PG_DATABASE,)
                cur.execute(query, params)

    def query(self, query_template: str, table_name: str = None, params: str = None):
        """PostgreSQLにクエリを実行する関数
        プレースホルダーを使用してパラメータ化されたクエリを使用することで、SQLインジェクションを防ぎます。
        ユーザー入力を直接query_templateに挿入することは避けてください。ユーザー入力を使用する場合は、常にSQLクエリのパラメータとして渡し、SQLインジェクション攻撃を防ぐためにプレースホルダーを使用してください。
        テーブル名やカラム名など、SQL文の構造に関わる部分を動的に変更する場合は、その値が信頼できるソースから来ていること、または適切に検証されていることを確認してください。
        ```python
        # クエリテンプレートの定義
        query_template = "SELECT * FROM {table_name} WHERE column_name = %s;"
        # 使用するテーブル名
        table_name = "your_table_name"
        # クエリをフォーマットしてテーブル名を挿入
        formatted_query = query_template.format(table_name=table_name)
        # クエリの実行
        cur.execute(formatted_query, (param_value,))
        ```
        """
        # テーブル名を動的に含むセーフなクエリを実行する
        if table_name:
            # テーブル名の安全性を確認
            # テーブル名が予め定義されたリストに含まれていることを確認
            print(table_name)
            print(self.allowed_tables)
            if table_name not in self.allowed_tables:
                raise ValueError(f"不正なテーブル名: {table_name}")
            # テーブル名が安全であると確認された後、クエリを動的に構築
            query = query_template.format(table_name=table_name)
        else:
            query = query
        # データベースに接続
        with psycopg2.connect(
            dbname=self.postgresConfig.PG_DATABASE,
            user=self.postgresConfig.PG_USER,
            password=self.postgresConfig.PG_PASSWORD,
            host=self.postgresConfig.PG_HOST,
            port=self.postgresConfig.PG_PORT,
        ) as conn:
            conn.autocommit = True
            # カーソルを作成
            with conn.cursor() as cur:
                # パラメータ化されたクエリを実行
                cur.execute(query, params)
                data = cur.fetchall()
                return data

    def get_data(
        self,
        key,
        query_template: str,
        table_name: str = "",
        params: tuple[str] = (),
    ):
        """キャッシュされたデータを取得する関数。キャッシュが存在しない場合はDBから取得してキャッシュする"""
        # Redisからデータを取得しようとする
        cached_data = self.r.get(key)
        if cached_data:
            print("キャッシュヒット")
            return cached_data
        else:
            print("キャッシュミス - DBからデータを取得")
            data = self.query(query_template, table_name, params)
            # 取得したデータをキャッシュに保存（例：有効期限60秒）
            self.r.setex(key, 60, str(data))
            return data


if __name__ == "__main__":
    env_info: EnvInfo = get_env_info(EnvInfo)
    postgresConfig = PostgresConfig(
        PG_USER=env_info.PG_USER, PG_PASSWORD=env_info.PG_PASSWORD
    )
    redisConfig = RedisConfig(REDIS_PASSWORD=env_info.REDIS_PASSWORD)
    manager = PostgreAndRedisManager(postgresConfig, redisConfig)
    key = f"{postgresConfig.PG_TABLE}_data"
    query_template = "SELECT * FROM {table_name} LIMIT %s;"
    table_name = postgresConfig.PG_TABLE
    params = (10,)
    data = manager.get_data(key, query_template, table_name, params)
    print(data)
