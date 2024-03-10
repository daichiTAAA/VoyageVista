from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

import api.schemas as schemas
import api.cruds as cruds
from api.db import get_db
from api.setup_logger import setup_logger

logger, log_decorator = setup_logger(__name__)

router_v1 = APIRouter(
    prefix="/articles",
    tags=["articles"],
    responses={404: {"description": "Not found"}},
)


@router_v1.post(
    "/", response_model=schemas.Article, status_code=status.HTTP_201_CREATED
)
async def create_article(
    article: schemas.ArticleCreate, db: AsyncSession = Depends(get_db)
):
    db_article = await cruds.create_article(db=db, article=article)
    if not db_article:
        logger.error("Article could not be created")
        raise HTTPException(status_code=400, detail="Article could not be created")
    return db_article


@router_v1.get("/", response_model=List[schemas.Article])
async def read_articles(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    articles = await cruds.get_articles(db, skip=skip, limit=limit)
    return articles


@router_v1.get("/{article_id}", response_model=schemas.Article)
async def read_article(article_id: int, db: AsyncSession = Depends(get_db)):
    db_article = await cruds.get_article(db, article_id=article_id)
    if db_article is None:
        logger.error(f"Article {article_id} not found")
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article


@router_v1.put("/{article_id}", response_model=schemas.Article)
async def update_article(
    article_id: int, article: schemas.ArticleUpdate, db: AsyncSession = Depends(get_db)
):
    db_article = await cruds.get_article(db, article_id=article_id)
    if db_article is None:
        logger.error(f"Article {article_id} not found")
        raise HTTPException(status_code=404, detail="Article not found")
    return await cruds.update_article(db=db, article=article, article_id=article_id)


@router_v1.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(article_id: int, db: AsyncSession = Depends(get_db)):
    success = await cruds.delete_article(db=db, article_id=article_id)
    if not success:
        logger.error(f"Article {article_id} not found")
        raise HTTPException(status_code=404, detail="Article not found")
    # 204 No Content ステータスコードを返すためにレスポンスボディは空
    return Response(content=None, status_code=status.HTTP_204_NO_CONTENT)


@router_v1.post(
    "/{article_id}/photos/",
    response_model=schemas.Photo,
    status_code=status.HTTP_201_CREATED,
)
async def create_photo_for_article(
    article_id: int, photo: schemas.PhotoCreate, db: AsyncSession = Depends(get_db)
):
    db_photo = await cruds.create_photo(db=db, photo=photo, article_id=article_id)
    if not db_photo:
        logger.error("Photo could not be created")
        raise HTTPException(status_code=400, detail="Photo could not be created")
    return db_photo


@router_v1.post(
    "/{article_id}/translations/",
    response_model=schemas.Translation,
    status_code=status.HTTP_201_CREATED,
)
async def create_translation_for_article(
    article_id: int,
    translation: schemas.TranslationCreate,
    db: AsyncSession = Depends(get_db),
):
    db_translation = await cruds.create_translation(
        db=db, translation=translation, article_id=article_id
    )
    if not db_translation:
        logger.error("Translation could not be created")
        raise HTTPException(status_code=400, detail="Translation could not be created")
    return db_translation


@router_v1.post(
    "/{article_id}/cultural_insights/",
    response_model=schemas.CulturalInsight,
    status_code=status.HTTP_201_CREATED,
)
async def create_cultural_insight_for_article(
    article_id: int,
    cultural_insight: schemas.CulturalInsightCreate,
    db: AsyncSession = Depends(get_db),
):
    db_cultural_insights = await cruds.create_cultural_insight(
        db=db, cultural_insight=cultural_insight, article_id=article_id
    )
    if not db_cultural_insights:
        logger.error("Cultural_insights could not be created")
        raise HTTPException(
            status_code=400, detail="Cultural_insights could not be created"
        )
    return db_cultural_insights
