import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from main import app
from api.db import Base, get_db
import api.models as models
import api.schemas as schemas
import api.cruds as cruds

pytestmark = pytest.mark.asyncio


async def test_create_article(async_client: AsyncClient, async_session: AsyncSession):
    article_data = {
        "title": "Test Article",
        "content": "This is a test article.",
        "status": "draft",
        "author_id": 1,
        "created_at": "2021-06-01T12:00:00",
        "updated_at": "2021-06-01T12:00:00",
    }
    response = await async_client.post("/v1/articles/", json=article_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == article_data["title"]
    assert data["content"] == article_data["content"]
    assert data["status"] == article_data["status"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


async def test_read_articles(async_client: AsyncClient, async_session: AsyncSession):
    articles = [
        schemas.ArticleCreate(
            title=f"Test Article {i}",
            content=f"Content {i}",
            status="draft",
            author_id=1,
        )
        for i in range(5)
    ]
    for article in articles:
        await cruds.create_article(db=async_session, article=article)

    response = await async_client.get("/v1/articles/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    for article, article_data in zip(data, articles):
        assert article["title"] == article_data.title
        assert article["content"] == article_data.content
        assert article["status"] == article_data.status


async def test_read_article(async_client: AsyncClient, async_session: AsyncSession):
    article = schemas.ArticleCreate(
        title="Test Article", content="Content", status="draft", author_id=1
    )
    db_article = await cruds.create_article(db=async_session, article=article)

    response = await async_client.get(f"/v1/articles/{db_article.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == db_article.id
    assert data["title"] == article.title
    assert data["content"] == article.content
    assert data["status"] == article.status


async def test_read_article_not_found(async_client: AsyncClient):
    response = await async_client.get("/v1/articles/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Article not found"


async def test_update_article(async_client: AsyncClient, async_session: AsyncSession):
    article = schemas.ArticleCreate(
        title="Test Article", content="Content", status="draft", author_id=1
    )
    db_article = await cruds.create_article(db=async_session, article=article)

    updated_article_data = {
        "title": "Updated Test Article",
        "content": "Updated Content",
        "status": "published",
    }

    response = await async_client.put(
        f"/v1/articles/{db_article.id}", json=updated_article_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == db_article.id
    assert data["title"] == updated_article_data["title"]
    assert data["content"] == updated_article_data["content"]
    assert data["status"] == updated_article_data["status"]


async def test_update_article_not_found(async_client: AsyncClient):
    updated_article_data = {
        "title": "Updated Test Article",
        "content": "Updated Content",
        "status": "published",
    }

    response = await async_client.put("/v1/articles/999", json=updated_article_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Article not found"


async def test_delete_article(async_client: AsyncClient, async_session: AsyncSession):
    article = schemas.ArticleCreate(
        title="Test Article", content="Content", status="draft", author_id=1
    )
    db_article = await cruds.create_article(db=async_session, article=article)
    response = await async_client.delete(f"/v1/articles/{db_article.id}")
    assert (
        response.status_code == 204
    )  # ステータスコードが 204 No Content であることを確認
    assert response.content == b""  # レスポンスボディが空であることを確認
    db_article = await cruds.get_article(db=async_session, article_id=db_article.id)
    assert db_article is None


async def test_delete_article_not_found(async_client: AsyncClient):
    response = await async_client.delete("/v1/articles/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Article not found"


async def test_create_photo_for_article(
    async_client: AsyncClient, async_session: AsyncSession
):
    article = schemas.ArticleCreate(
        title="Test Article", content="Content", status="draft", author_id=1
    )
    db_article = await cruds.create_article(db=async_session, article=article)

    photo_data = {"file_path": "test/path/photo.jpg", "description": "Test photo"}

    response = await async_client.post(
        f"/v1/articles/{db_article.id}/photos/", json=photo_data
    )
    assert response.status_code == 201
    data = response.json()
    assert data["file_path"] == photo_data["file_path"]
    assert data["description"] == photo_data["description"]
    assert data["article_id"] == db_article.id


async def test_create_translation_for_article(
    async_client: AsyncClient, async_session: AsyncSession
):
    article = schemas.ArticleCreate(
        title="Test Article", content="Content", status="draft", author_id=1
    )
    db_article = await cruds.create_article(db=async_session, article=article)

    translation_data = {
        "language": "en",
        "title": "Test Translation",
        "description": "This is a test translation.",
        "translated_text": "Translated text of the test article.",
    }

    response = await async_client.post(
        f"/v1/articles/{db_article.id}/translations/", json=translation_data
    )
    assert response.status_code == 201
    data = response.json()
    assert data["language"] == translation_data["language"]
    assert data["title"] == translation_data["title"]
    assert data["description"] == translation_data["description"]
    assert data["translated_text"] == translation_data["translated_text"]
    assert data["article_id"] == db_article.id


async def test_create_cultural_insight_for_article(
    async_client: AsyncClient, async_session: AsyncSession
):
    article = schemas.ArticleCreate(
        title="Test Article", content="Content", status="draft", author_id=1
    )
    db_article = await cruds.create_article(db=async_session, article=article)

    cultural_insight_data = {"content": "This is a test cultural insight."}

    response = await async_client.post(
        f"/v1/articles/{db_article.id}/cultural_insights/", json=cultural_insight_data
    )
    assert response.status_code == 201
    data = response.json()
    assert data["content"] == cultural_insight_data["content"]
    assert data["article_id"] == db_article.id
