from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import cruds, schemas
from db import SessionLocal

router = APIRouter(
    prefix="/articles",
    tags=["articles"],
    responses={404: {"description": "Not found"}},
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.Article)
def create_article(article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    return cruds.create_article(db=db, article=article)


@router.get("/", response_model=List[schemas.Article])
def read_articles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    articles = cruds.get_articles(db, skip=skip, limit=limit)
    return articles


@router.get("/{article_id}", response_model=schemas.Article)
def read_article(article_id: int, db: Session = Depends(get_db)):
    db_article = cruds.get_article(db, article_id=article_id)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article


@router.put("/{article_id}", response_model=schemas.Article)
def update_article(
    article_id: int, article: schemas.ArticleCreate, db: Session = Depends(get_db)
):
    db_article = cruds.get_article(db, article_id=article_id)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return cruds.update_article(db=db, article=article, article_id=article_id)


@router.delete("/{article_id}", response_model=schemas.Article)
def delete_article(article_id: int, db: Session = Depends(get_db)):
    db_article = cruds.get_article(db, article_id=article_id)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return cruds.delete_article(db=db, article_id=article_id)


@router.post("/{article_id}/photos/", response_model=schemas.Photo)
def create_photo_for_article(
    article_id: int, photo: schemas.PhotoCreate, db: Session = Depends(get_db)
):
    return cruds.create_photo(db=db, photo=photo, article_id=article_id)


@router.post("/{article_id}/translations/", response_model=schemas.Translation)
def create_translation_for_article(
    article_id: int,
    translation: schemas.TranslationCreate,
    db: Session = Depends(get_db),
):
    return cruds.create_translation(
        db=db, translation=translation, article_id=article_id
    )


@router.post("/{article_id}/cultural_insights/", response_model=schemas.CulturalInsight)
def create_cultural_insight_for_article(
    article_id: int,
    cultural_insight: schemas.CulturalInsightCreate,
    db: Session = Depends(get_db),
):
    return cruds.create_cultural_insight(
        db=db, cultural_insight=cultural_insight, article_id=article_id
    )
