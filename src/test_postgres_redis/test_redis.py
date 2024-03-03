import os
from typing import Type, TypeVar

from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError, TypeAdapter
import redis


class EnvInfo(BaseModel):
    REDIS_PASSWORD: str


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

password = env.REDIS_PASSWORD

# Redis に接続します
r = redis.Redis(host="localhost", port=6379, db=0, password=password)

# 'hoge' というキーで 'moge' という値を追加します
r.set("hoge", "moge")

# 追加した値を取得して表示します
hoge = r.get("hoge")
print(hoge.decode())

# 追加した値を削除します
result = r.delete("hoge")
