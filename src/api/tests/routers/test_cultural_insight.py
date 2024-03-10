import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from main import app
import api.schemas as schemas
import api.cruds as cruds

pytestmark = pytest.mark.asyncio


async def test_create_cultural_insight(
    async_client: AsyncClient, async_session: AsyncSession
):
    article = schemas.ArticleCreate(
        title="Test Article", content="Test content", status="draft", author_id=1
    )
    db_article = await cruds.create_article(db=async_session, article=article)

    cultural_insight_data = {"content": "Test cultural insight"}
    response = await async_client.post(
        f"/v1/cultural_insights/?article_id={db_article.id}", json=cultural_insight_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == cultural_insight_data["content"]
    assert data["article_id"] == db_article.id
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


async def test_read_cultural_insights(
    async_client: AsyncClient, async_session: AsyncSession
):
    article = schemas.ArticleCreate(
        title="Test Article", content="Test content", status="draft", author_id=1
    )
    db_article = await cruds.create_article(db=async_session, article=article)

    cultural_insights = [
        schemas.CulturalInsightCreate(content=f"Test cultural insight {i}")
        for i in range(5)
    ]
    for insight in cultural_insights:
        await cruds.create_cultural_insight(
            db=async_session, cultural_insight=insight, article_id=db_article.id
        )

    response = await async_client.get("/v1/cultural_insights/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    for insight, insight_data in zip(data, cultural_insights):
        assert insight["content"] == insight_data.content


async def test_read_cultural_insight(
    async_client: AsyncClient, async_session: AsyncSession
):
    article = schemas.ArticleCreate(
        title="Test Article", content="Test content", status="draft", author_id=1
    )
    db_article = await cruds.create_article(db=async_session, article=article)

    cultural_insight = schemas.CulturalInsightCreate(content="Test cultural insight")
    db_insight = await cruds.create_cultural_insight(
        db=async_session, cultural_insight=cultural_insight, article_id=db_article.id
    )

    response = await async_client.get(f"/v1/cultural_insights/{db_insight.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == db_insight.id
    assert data["content"] == cultural_insight.content
    assert data["article_id"] == db_article.id


async def test_read_cultural_insight_not_found(async_client: AsyncClient):
    response = await async_client.get("/v1/cultural_insights/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Cultural insight not found"


async def test_update_cultural_insight(
    async_client: AsyncClient, async_session: AsyncSession
):
    article = schemas.ArticleCreate(
        title="Test Article", content="Test content", status="draft", author_id=1
    )
    db_article = await cruds.create_article(db=async_session, article=article)

    cultural_insight = schemas.CulturalInsightCreate(content="Test cultural insight")
    db_insight = await cruds.create_cultural_insight(
        db=async_session, cultural_insight=cultural_insight, article_id=db_article.id
    )

    updated_insight_data = {"content": "Updated cultural insight"}
    response = await async_client.put(
        f"/v1/cultural_insights/{db_insight.id}", json=updated_insight_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == db_insight.id
    assert data["content"] == updated_insight_data["content"]
    assert data["article_id"] == db_article.id


async def test_update_cultural_insight_not_found(async_client: AsyncClient):
    updated_insight_data = {"content": "Updated cultural insight"}
    response = await async_client.put(
        "/v1/cultural_insights/999", json=updated_insight_data
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Cultural insight not found"


async def test_delete_cultural_insight(
    async_client: AsyncClient, async_session: AsyncSession
):
    article = schemas.ArticleCreate(
        title="Test Article", content="Test content", status="draft", author_id=1
    )
    db_article = await cruds.create_article(db=async_session, article=article)

    cultural_insight = schemas.CulturalInsightCreate(content="Test cultural insight")
    db_insight = await cruds.create_cultural_insight(
        db=async_session, cultural_insight=cultural_insight, article_id=db_article.id
    )

    response = await async_client.delete(f"/v1/cultural_insights/{db_insight.id}")
    assert (
        response.status_code == 204
    )  # ステータスコードが 204 No Content であることを確認
    assert response.content == b""  # レスポンスボディが空であることを確認
    db_insight = await cruds.get_cultural_insight(
        db=async_session, cultural_insight_id=db_insight.id
    )
    assert db_insight is None


async def test_delete_cultural_insight_not_found(async_client: AsyncClient):
    response = await async_client.delete("/v1/cultural_insights/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Cultural insight not found"
