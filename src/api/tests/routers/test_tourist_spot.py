import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from api.db import get_db, Base
from main import app
import api.models as models
import api.schemas as schemas
import api.cruds as cruds

pytestmark = pytest.mark.asyncio


async def test_create_tourist_spot(async_client: AsyncClient):
    tourist_spot_data = {
        "name": "Test Tourist Spot",
        "location": "Test Location",
        "description": "Test Description",
        "average_stay_time": 2.5,
    }
    response = await async_client.post("/v1/tourist_spots/", json=tourist_spot_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == tourist_spot_data["name"]
    assert data["location"] == tourist_spot_data["location"]
    assert data["description"] == tourist_spot_data["description"]
    assert data["average_stay_time"] == tourist_spot_data["average_stay_time"]


async def test_read_tourist_spots(async_client: AsyncClient):
    response = await async_client.get("/v1/tourist_spots/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


async def test_read_tourist_spot(
    async_client: AsyncClient, async_session: AsyncSession
):
    tourist_spot_request = schemas.TouristSpotCreate(
        name="Test Tourist Spot",
        location="Test Location",
        description="Test Description",
        average_stay_time=2.5,
    )
    tourist_spot = await cruds.create_tourist_spot(async_session, tourist_spot_request)

    response = await async_client.get(f"/v1/tourist_spots/{tourist_spot.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == tourist_spot.id
    assert data["name"] == tourist_spot.name
    assert data["location"] == tourist_spot.location
    assert data["description"] == tourist_spot.description
    assert data["average_stay_time"] == tourist_spot.average_stay_time


async def test_update_tourist_spot(
    async_client: AsyncClient, async_session: AsyncSession
):
    tourist_spot_request = schemas.TouristSpotCreate(
        name="Test Tourist Spot",
        location="Test Location",
        description="Test Description",
        average_stay_time=2.5,
    )
    tourist_spot = await cruds.create_tourist_spot(async_session, tourist_spot_request)

    update_data = {
        "name": "Updated Tourist Spot",
        "location": "Updated Location",
        "description": "Updated Description",
        "average_stay_time": 3.0,
    }
    response = await async_client.put(
        f"/v1/tourist_spots/{tourist_spot.id}", json=update_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == tourist_spot.id
    assert data["name"] == update_data["name"]
    assert data["location"] == update_data["location"]
    assert data["description"] == update_data["description"]
    assert data["average_stay_time"] == update_data["average_stay_time"]


async def test_delete_tourist_spot(
    async_client: AsyncClient, async_session: AsyncSession
):
    tourist_spot_request = schemas.TouristSpotCreate(
        name="Test Tourist Spot",
        location="Test Location",
        description="Test Description",
        average_stay_time=2.5,
    )
    tourist_spot = await cruds.create_tourist_spot(async_session, tourist_spot_request)

    response = await async_client.delete(f"/v1/tourist_spots/{tourist_spot.id}")
    assert (
        response.status_code == 204
    )  # ステータスコードが 204 No Content であることを確認
    assert response.content == b""  # レスポンスボディが空であることを確認
    db_tourist_spot = await cruds.get_tourist_spot(
        db=async_session, tourist_spot_id=tourist_spot.id
    )
    assert db_tourist_spot is None


async def test_read_associated_articles(
    async_client: AsyncClient, async_session: AsyncSession
):
    tourist_spot_request = schemas.TouristSpotCreate(
        name="Test Tourist Spot",
        location="Test Location",
        description="Test Description",
        average_stay_time=2.5,
    )
    tourist_spot = await cruds.create_tourist_spot(async_session, tourist_spot_request)

    article = schemas.ArticleCreate(
        title="Test Article", content="Content", status="draft", author_id=1
    )
    article = await cruds.create_article(db=async_session, article=article)

    await cruds.link_article_to_tourist_spot(
        db=async_session, tourist_spot_id=tourist_spot.id, article_id=article.id
    )

    response = await async_client.get(f"/v1/tourist_spots/{tourist_spot.id}/articles")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["article_id"] == article.id
    assert data[0]["tourist_spot_id"] == tourist_spot.id


async def test_create_link_article_to_tourist_spot(
    async_client: AsyncClient, async_session: AsyncSession
):
    tourist_spot_request = schemas.TouristSpotCreate(
        name="Test Tourist Spot",
        location="Test Location",
        description="Test Description",
        average_stay_time=2.5,
    )
    tourist_spot = await cruds.create_tourist_spot(async_session, tourist_spot_request)

    article = schemas.ArticleCreate(
        title="Test Article", content="Content", status="draft", author_id=1
    )
    article = await cruds.create_article(db=async_session, article=article)

    response = await async_client.post(
        f"/v1/tourist_spots/{tourist_spot.id}/articles/{article.id}"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["article_id"] == article.id
    assert data["tourist_spot_id"] == tourist_spot.id


async def test_delete_link_article_from_tourist_spot(
    async_client: AsyncClient, async_session: AsyncSession
):
    tourist_spot_request = schemas.TouristSpotCreate(
        name="Test Tourist Spot",
        location="Test Location",
        description="Test Description",
        average_stay_time=2.5,
    )
    tourist_spot = await cruds.create_tourist_spot(async_session, tourist_spot_request)

    article = schemas.ArticleCreate(
        title="Test Article", content="Content", status="draft", author_id=1
    )
    article = await cruds.create_article(db=async_session, article=article)

    association_request = schemas.ArticleTouristSpotCreate(
        article_id=article.id, tourist_spot_id=tourist_spot.id
    )
    await cruds.link_article_to_tourist_spot(
        db=async_session, association=association_request
    )

    response = await async_client.delete(
        f"/v1/tourist_spots/{tourist_spot.id}/articles/{article.id}"
    )
    assert response.status_code == 204

    deleted_association = await async_session.get(
        models.ArticleTouristSpot, (article.id, tourist_spot.id)
    )
    assert deleted_association is None


async def test_update_association(
    async_client: AsyncClient, async_session: AsyncSession
):
    tourist_spot_request = schemas.TouristSpotCreate(
        name="Test Tourist Spot",
        location="Test Location",
        description="Test Description",
        average_stay_time=2.5,
    )
    tourist_spot = await cruds.create_tourist_spot(async_session, tourist_spot_request)

    article = schemas.ArticleCreate(
        title="Test Article", content="Content", status="draft", author_id=1
    )
    article = await cruds.create_article(db=async_session, article=article)

    association_request = schemas.ArticleTouristSpotCreate(
        article_id=article.id, tourist_spot_id=tourist_spot.id
    )
    association = await cruds.link_article_to_tourist_spot(
        db=async_session, association=association_request
    )
    async_session.add(association)
    await async_session.commit()

    response = await async_client.put(
        f"/v1/tourist_spots/{tourist_spot.id}/articles/{article.id}"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["article_id"] == article.id
    assert data["tourist_spot_id"] == tourist_spot.id
