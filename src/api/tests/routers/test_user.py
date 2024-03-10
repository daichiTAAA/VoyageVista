import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from api.db import Base, get_db
from main import app
import api.models as models
import api.schemas as schemas
import api.cruds as cruds

pytestmark = pytest.mark.asyncio


async def test_create_user(async_client: AsyncClient):
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword",
        "role": "user",
    }
    response = await async_client.post("/v1/users/", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]
    assert data["role"] == user_data["role"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data
    assert "password" not in data


async def test_create_user_already_registered(
    async_client: AsyncClient, async_session: AsyncSession
):
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword",
        "role": "user",
    }
    await cruds.create_user(async_session, schemas.UserCreate(**user_data))
    response = await async_client.post("/v1/users/", json=user_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


async def test_read_users(async_client: AsyncClient, async_session: AsyncSession):
    users = [
        schemas.UserCreate(
            username=f"testuser{i}",
            email=f"testuser{i}@example.com",
            password="testpassword",
            role="user",
        )
        for i in range(5)
    ]
    for user in users:
        await cruds.create_user(db=async_session, user=user)

    response = await async_client.get("/v1/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    for user, user_data in zip(data, users):
        assert user["email"] == user_data.email
        assert user["username"] == user_data.username
        assert user["role"] == user_data.role


async def test_read_user(async_client: AsyncClient, async_session: AsyncSession):
    user = schemas.UserCreate(
        username="testuser",
        email="testuser@example.com",
        password="testpassword",
        role="user",
    )
    db_user = await cruds.create_user(db=async_session, user=user)

    response = await async_client.get(f"/v1/users/{db_user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == db_user.id
    assert data["email"] == user.email
    assert data["username"] == user.username
    assert data["role"] == user.role


async def test_read_user_not_found(async_client: AsyncClient):
    response = await async_client.get("/v1/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


async def test_update_user(async_client: AsyncClient, async_session: AsyncSession):
    user = schemas.UserCreate(
        username="testuser",
        email="testuser@example.com",
        password="testpassword",
        role="user",
    )
    db_user = await cruds.create_user(db=async_session, user=user)

    updated_user_data = {
        "username": "updated_testuser",
        "email": "updated_testuser@example.com",
        "password": "updated_testpassword",
        "role": "admin",
    }

    response = await async_client.put(f"/v1/users/{db_user.id}", json=updated_user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == db_user.id
    assert data["email"] == updated_user_data["email"]
    assert data["username"] == updated_user_data["username"]
    assert data["role"] == updated_user_data["role"]


async def test_update_user_not_found(async_client: AsyncClient):
    updated_user_data = {
        "username": "updated_testuser",
        "email": "updated_testuser@example.com",
        "password": "updated_testpassword",
        "role": "admin",
    }

    response = await async_client.put("/v1/users/999", json=updated_user_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


async def test_delete_user(async_client: AsyncClient, async_session: AsyncSession):
    user = schemas.UserCreate(
        username="testuser",
        email="testuser@example.com",
        password="testpassword",
        role="user",
    )
    db_user = await cruds.create_user(db=async_session, user=user)

    response = await async_client.delete(f"/v1/users/{db_user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == db_user.id
    assert data["email"] == user.email
    assert data["username"] == user.username
    assert data["role"] == user.role

    db_user = await cruds.get_user(db=async_session, user_id=db_user.id)
    assert db_user is None


async def test_delete_user_not_found(async_client: AsyncClient):
    response = await async_client.delete("/v1/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


async def test_read_user_articles(
    async_client: AsyncClient, async_session: AsyncSession
):
    user = schemas.UserCreate(
        username="testuser",
        email="testuser@example.com",
        password="testpassword",
        role="user",
    )
    db_user = await cruds.create_user(db=async_session, user=user)

    articles = [
        schemas.ArticleCreate(
            title=f"Test Article {i}",
            content=f"Content {i}",
            status="draft",
            author_id=db_user.id,
        )
        for i in range(5)
    ]
    for article in articles:
        await cruds.create_article(db=async_session, article=article)

    response = await async_client.get(f"/v1/users/{db_user.id}/articles/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    for article, article_data in zip(data, articles):
        assert article["title"] == article_data.title
        assert article["content"] == article_data.content
        assert article["status"] == article_data.status
