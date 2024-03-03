import os
from typing import Type, TypeVar

from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import DictCursor
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


# .envファイルを探して、あれば読み込む
load_dotenv()

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


env: EnvInfo = create_instance_from_env(EnvInfo)
postgresConfig: PostgresConfig = PostgresConfig(
    PG_USER=env.PG_USER, PG_PASSWORD=env.PG_PASSWORD
)
redisConfig: RedisConfig = RedisConfig(REDIS_PASSWORD=env.REDIS_PASSWORD)


def get_data_from_pg(query):
    """PostgreSQLからデータを取得する関数"""
    pg_cursor.execute(query)
    result = pg_cursor.fetchall()
    return result


def get_data(key, query):
    """キャッシュされたデータを取得する関数。キャッシュが存在しない場合はDBから取得してキャッシュする"""
    # Redisからデータを取得しようとする
    cached_data = r.get(key)
    if cached_data:
        print("キャッシュヒット")
        return cached_data
    else:
        print("キャッシュミス - DBからデータを取得")
        data = get_data_from_pg(query)
        # 取得したデータをキャッシュに保存（例：有効期限60秒）
        r.setex(key, 60, str(data))
        return data


if __name__ == "__main__":
    # Redisに接続
    r = redis.Redis(
        host=redisConfig.REDIS_HOST,
        port=redisConfig.REDIS_PORT,
        password=redisConfig.REDIS_PASSWORD,
        decode_responses=True,
    )

    # PostgreSQLに接続
    pg_conn = psycopg2.connect(
        dbname=postgresConfig.PG_DATABASE,
        user=postgresConfig.PG_USER,
        password=postgresConfig.PG_PASSWORD,
        host=postgresConfig.PG_HOST,
    )
    pg_cursor = pg_conn.cursor(cursor_factory=DictCursor)

    # 使用例
    query = f"SELECT * FROM {postgresConfig.PG_TABLE} LIMIT 10;"
    key = f"{postgresConfig.PG_TABLE}_data"
    data = get_data(key, query)
    print(data)

    # データベース接続を閉じる
    pg_cursor.close()
    pg_conn.close()
