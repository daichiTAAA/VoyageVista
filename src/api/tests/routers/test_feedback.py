import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

import api.schemas as schemas
import api.models as models
import api.cruds as cruds
from main import app

pytestmark = pytest.mark.asyncio


async def test_create_feedback(async_client: AsyncClient, async_session: AsyncSession):
    user_request = schemas.UserCreate(
        username="testuser",
        email="testuser@example.com",
        role="user",
        password="testpassword",
    )
    user = await cruds.create_user(async_session, user_request)

    article_request = schemas.ArticleCreate(
        title="Test Article", content="Test content", status="draft", author_id=1
    )
    article = await cruds.create_article(async_session, article_request)

    feedback_data = {"content": "Test feedback"}
    response = await async_client.post(
        f"/v1/feedbacks/?user_id={user.id}&article_id={article.id}", json=feedback_data
    )
    assert response.status_code == 201
    data = response.json()
    assert data["content"] == feedback_data["content"]
    assert data["user_id"] == user.id
    assert data["article_id"] == article.id


async def test_read_feedbacks(async_client: AsyncClient, async_session: AsyncSession):
    user_request = schemas.UserCreate(
        username="testuser",
        email="testuser@example.com",
        role="user",
        password="testpassword",
    )
    user = await cruds.create_user(async_session, user_request)

    article_request = schemas.ArticleCreate(
        title="Test Article", content="Test content", status="draft", author_id=1
    )
    article = await cruds.create_article(async_session, article_request)

    for i in range(5):
        feedback_request = schemas.FeedbackCreate(content=f"Test feedback {i}")
        feedback = await cruds.create_feedback(
            async_session, feedback_request, user_id=user.id, article_id=article.id
        )

    response = await async_client.get("/v1/feedbacks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5


async def test_read_feedback(async_client: AsyncClient, async_session: AsyncSession):
    user_request = schemas.UserCreate(
        username="testuser",
        email="testuser@example.com",
        role="user",
        password="testpassword",
    )
    user = await cruds.create_user(async_session, user_request)

    article_request = schemas.ArticleCreate(
        title="Test Article", content="Test content", status="draft", author_id=1
    )
    article = await cruds.create_article(async_session, article_request)

    feedback_request = schemas.FeedbackCreate(content="Test feedback")
    feedback = await cruds.create_feedback(
        async_session, feedback_request, user_id=user.id, article_id=article.id
    )

    response = await async_client.get(f"/v1/feedbacks/{feedback.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == feedback.id
    assert data["content"] == feedback.content
    assert data["user_id"] == user.id
    assert data["article_id"] == article.id


async def test_update_feedback(async_client: AsyncClient, async_session: AsyncSession):
    user_request = schemas.UserCreate(
        username="testuser",
        email="testuser@example.com",
        role="user",
        password="testpassword",
    )
    user = await cruds.create_user(async_session, user_request)

    article_request = schemas.ArticleCreate(
        title="Test Article", content="Test content", status="draft", author_id=1
    )
    article = await cruds.create_article(async_session, article_request)

    feedback_request = schemas.FeedbackCreate(content="Test feedback")
    feedback = await cruds.create_feedback(
        async_session, feedback_request, user_id=user.id, article_id=article.id
    )

    update_data = {"content": "Updated feedback"}
    response = await async_client.put(f"/v1/feedbacks/{feedback.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == feedback.id
    assert data["content"] == update_data["content"]
    assert data["user_id"] == user.id
    assert data["article_id"] == article.id


async def test_delete_feedback(async_client: AsyncClient, async_session: AsyncSession):
    user_request = schemas.UserCreate(
        username="testuser",
        email="testuser@example.com",
        role="user",
        password="testpassword",
    )
    user = await cruds.create_user(async_session, user_request)

    article_request = schemas.ArticleCreate(
        title="Test Article", content="Test content", status="draft", author_id=1
    )
    article = await cruds.create_article(async_session, article_request)

    feedback_request = schemas.FeedbackCreate(content="Test feedback")
    feedback = await cruds.create_feedback(
        async_session, feedback_request, user_id=user.id, article_id=article.id
    )

    response = await async_client.delete(f"/v1/feedbacks/{feedback.id}")
    assert (
        response.status_code == 204
    )  # ステータスコードが 204 No Content であることを確認
    assert response.content == b""  # レスポンスボディが空であることを確認
    db_feedback = await cruds.get_feedback(db=async_session, feedback_id=feedback.id)
    assert db_feedback is None
