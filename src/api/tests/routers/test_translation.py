import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

import api.schemas as schemas
import api.cruds as cruds
import api.models as models
from main import app

pytestmark = pytest.mark.asyncio


async def test_create_translation(
    async_client: AsyncClient, async_session: AsyncSession
):
    article_request = schemas.ArticleCreate(
        title="Test Article", content="Test content", status="draft", author_id=1
    )
    article = await cruds.create_article(db=async_session, article=article_request)

    translation_data = {
        "language": "en",
        "title": "Test Translation",
        "description": "Test translation description",
        "translated_text": "Translated text",
    }
    response = await async_client.post(
        f"/v1/translations/?article_id={article.id}", json=translation_data
    )
    assert response.status_code == 201
    data = response.json()
    assert data["language"] == translation_data["language"]
    assert data["title"] == translation_data["title"]
    assert data["description"] == translation_data["description"]
    assert data["translated_text"] == translation_data["translated_text"]
    assert data["article_id"] == article.id


async def test_read_translations(
    async_client: AsyncClient, async_session: AsyncSession
):
    article_request = schemas.ArticleCreate(
        title="Test Article", content="Test content", status="draft", author_id=1
    )
    article = await cruds.create_article(db=async_session, article=article_request)

    for i in range(5):
        translation = schemas.TranslationCreate(
            language=f"language{i}",
            title=f"Title {i}",
            description=f"Description {i}",
            translated_text=f"Translated text {i}",
        )
        await cruds.create_translation(
            db=async_session, translation=translation, article_id=article.id
        )

    response = await async_client.get("/v1/translations/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5


async def test_read_translation(async_client: AsyncClient, async_session: AsyncSession):
    article_request = schemas.ArticleCreate(
        title="Test Article", content="Test content", status="draft", author_id=1
    )
    article = await cruds.create_article(db=async_session, article=article_request)

    translation_request = schemas.TranslationCreate(
        language="en",
        title="Test Translation",
        description="Test translation description",
        translated_text="Translated text",
    )
    translation = await cruds.create_translation(
        db=async_session, translation=translation_request, article_id=article.id
    )

    response = await async_client.get(f"/v1/translations/{translation.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == translation.id
    assert data["language"] == translation.language
    assert data["title"] == translation.title
    assert data["description"] == translation.description
    assert data["translated_text"] == translation.translated_text
    assert data["article_id"] == article.id


async def test_update_translation(
    async_client: AsyncClient, async_session: AsyncSession
):
    article_request = schemas.ArticleCreate(
        title="Test Article", content="Test content", status="draft", author_id=1
    )
    article = await cruds.create_article(db=async_session, article=article_request)

    translation_request = schemas.TranslationCreate(
        language="en",
        title="Test Translation",
        description="Test translation description",
        translated_text="Translated text",
    )
    translation = await cruds.create_translation(
        db=async_session, translation=translation_request, article_id=article.id
    )

    update_data = {
        "language": "fr",
        "title": "Updated Translation",
        "description": "Updated translation description",
        "translated_text": "Updated translated text",
    }
    response = await async_client.put(
        f"/v1/translations/{translation.id}", json=update_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == translation.id
    assert data["language"] == update_data["language"]
    assert data["title"] == update_data["title"]
    assert data["description"] == update_data["description"]
    assert data["translated_text"] == update_data["translated_text"]
    assert data["article_id"] == article.id


async def test_delete_translation(
    async_client: AsyncClient, async_session: AsyncSession
):
    article_request = schemas.ArticleCreate(
        title="Test Article", content="Test content", status="draft", author_id=1
    )
    article = await cruds.create_article(db=async_session, article=article_request)

    translation_request = schemas.TranslationCreate(
        language="en",
        title="Test Translation",
        description="Test translation description",
        translated_text="Translated text",
    )
    translation = await cruds.create_translation(
        db=async_session, translation=translation_request, article_id=article.id
    )

    response = await async_client.delete(f"/v1/translations/{translation.id}")
    assert response.status_code == 204

    translation = await cruds.get_translation(
        db=async_session, translation_id=translation.id
    )
    assert translation is None
