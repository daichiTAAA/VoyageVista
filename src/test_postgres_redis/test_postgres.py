import os
from typing import Type, TypeVar

from dotenv import load_dotenv
import psycopg2
from pydantic import BaseModel, ValidationError, TypeAdapter


class EnvInfo(BaseModel):
    PG_VERSION: str
    PG_CONTAINER_NAME: str
    PG_HOST: str
    PG_USER: str
    PG_PASSWORD: str


class PostgresConfig(BaseModel):
    PG_USER: str
    PG_PASSWORD: str
    PG_HOST: str = "localhost"
    PG_PORT: str = "5432"
    PG_DATABASE: str = "test_db"
    PG_TABLE: str = "test_table"


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

# データベースに接続
conn = psycopg2.connect(
    dbname="postgres",
    user=postgresConfig.PG_USER,
    password=postgresConfig.PG_PASSWORD,
    host=postgresConfig.PG_HOST,
    port=postgresConfig.PG_PORT,
)
conn.autocommit = True

# カーソルを作成
cur = conn.cursor()

# 新しいデータベースを作成（既に存在する場合は不要）
# cur.execute("CREATE DATABASE " + postgresConfig.PG_DATABASE)

# 新しいデータベースに接続
conn.close()
conn = psycopg2.connect(
    dbname=postgresConfig.PG_DATABASE,
    user=postgresConfig.PG_USER,
    password=postgresConfig.PG_PASSWORD,
    host=postgresConfig.PG_HOST,
    port=postgresConfig.PG_PORT,
)
conn.autocommit = True
cur = conn.cursor()

# 新しいテーブルを作成
cur.execute(
    f"""
    CREATE TABLE IF NOT EXISTS {postgresConfig.PG_TABLE} (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        age INT
    )
"""
)

# テーブルにレコードを挿入
cur.execute(
    f"""
    INSERT INTO {postgresConfig.PG_TABLE} (name, age) VALUES
    ('Alice', 30),
    ('Bob', 25),
    ('Charlie', 35)
"""
)

# レコードを取得
cur.execute(f"SELECT * FROM {postgresConfig.PG_TABLE}")
rows = cur.fetchall()
for row in rows:
    print(row)

# 接続を閉じる
cur.close()
conn.close()
