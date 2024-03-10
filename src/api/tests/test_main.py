"""
test_main.py: 
アプリケーション全体や、アプリケーションレベルでの機能の統合テストを記述します。
これには、アプリケーションが起動すること、全体的なルートが期待どおりに機能すること、
または複数のコンポーネント間のインタラクションが正しく行われることを検証するテストが含まれるかもしれません。

tests/routers/*.py: こちらは 各エンドポイント（およびそれに関連するエンドポイント）に特化したテストを記述します。
これには、作成、詳細の取得、更新、削除など、各エンドポイントに対する具体的なリクエストと期待されるレスポンスのテストが含まれます。
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from main import app

pytestmark = pytest.mark.asyncio


async def test_health_check(async_client: AsyncClient):
    response = await async_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_root(async_client: AsyncClient):
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Japan Tourism Info API"}
