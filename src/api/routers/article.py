from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

import cruds, schemas
from db import SessionLocal
from setup_logger import setup_logger

logger, log_decorator = setup_logger(__name__)

router_v1 = APIRouter(
    prefix="/articles",
    tags=["articles"],
    responses={404: {"description": "Not found"}},
)


async def get_db():
    async with SessionLocal() as session:
        yield session


@router_v1.post("/", response_model=schemas.Article)
async def create_article(
    article: schemas.ArticleCreate, db: AsyncSession = Depends(get_db)
):
    return await cruds.create_article(db=db, article=article)


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
    article_id: int, article: schemas.ArticleCreate, db: AsyncSession = Depends(get_db)
):
    db_article = await cruds.get_article(db, article_id=article_id)
    if db_article is None:
        logger.error(f"Article {article_id} not found")
        raise HTTPException(status_code=404, detail="Article not found")
    return await cruds.update_article(db=db, article=article, article_id=article_id)


@router_v1.delete("/{article_id}", response_model=schemas.Article)
async def delete_article(article_id: int, db: AsyncSession = Depends(get_db)):
    db_article = await cruds.get_article(db, article_id=article_id)
    if db_article is None:
        logger.error(f"Article {article_id} not found")
        raise HTTPException(status_code=404, detail="Article not found")
    return await cruds.delete_article(db=db, article_id=article_id)


@router_v1.post("/{article_id}/photos/", response_model=schemas.Photo)
async def create_photo_for_article(
    article_id: int, photo: schemas.PhotoCreate, db: AsyncSession = Depends(get_db)
):
    return await cruds.create_photo(db=db, photo=photo, article_id=article_id)


@router_v1.post("/{article_id}/translations/", response_model=schemas.Translation)
async def create_translation_for_article(
    article_id: int,
    translation: schemas.TranslationCreate,
    db: AsyncSession = Depends(get_db),
):
    return await cruds.create_translation(
        db=db, translation=translation, article_id=article_id
    )


@router_v1.post(
    "/{article_id}/cultural_insights/", response_model=schemas.CulturalInsight
)
async def create_cultural_insight_for_article(
    article_id: int,
    cultural_insight: schemas.CulturalInsightCreate,
    db: AsyncSession = Depends(get_db),
):
    return await cruds.create_cultural_insight(
        db=db, cultural_insight=cultural_insight, article_id=article_id
    )
