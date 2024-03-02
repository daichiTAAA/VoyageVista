import os
from typing import Type, TypeVar

from dotenv import load_dotenv
import psycopg2
from pydantic import BaseModel, ValidationError, TypeAdapter


class Envinfo(BaseModel):
    POSTGRES_VERSION: str
    CONTAINER_NAME: str
    HOSTNAME: str
    USER_NAME: str
    USER_PASS: str


class PostgresConfig(BaseModel):
    user: str
    password: str
    host: str = "localhost"
    port: str = "5432"
    database: str = "test_db"


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


env: Envinfo = create_instance_from_env(Envinfo)
postresConfig: PostgresConfig = PostgresConfig(
    user=env.USER_NAME, password=env.USER_PASS
)

# データベースに接続
conn = psycopg2.connect(
    dbname="postgres",
    user=postresConfig.user,
    password=postresConfig.password,
    host=postresConfig.host,
    port=postresConfig.port,
)
conn.autocommit = True

# カーソルを作成
cur = conn.cursor()

# 新しいデータベースを作成（既に存在する場合は不要）
# cur.execute("CREATE DATABASE " + postresConfig.database)

# 新しいデータベースに接続
conn.close()
conn = psycopg2.connect(
    dbname=postresConfig.database,
    user=postresConfig.user,
    password=postresConfig.password,
    host=postresConfig.host,
    port=postresConfig.port,
)
conn.autocommit = True
cur = conn.cursor()

# 新しいテーブルを作成
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS test_table (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        age INT
    )
"""
)

# テーブルにレコードを挿入
cur.execute(
    """
    INSERT INTO test_table (name, age) VALUES
    ('Alice', 30),
    ('Bob', 25),
    ('Charlie', 35)
"""
)

# レコードを取得
cur.execute("SELECT * FROM test_table")
rows = cur.fetchall()
for row in rows:
    print(row)

# 接続を閉じる
cur.close()
conn.close()
