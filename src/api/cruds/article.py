from sqlalchemy.orm import Session

import models, schemas


def get_article(db: Session, article_id: int):
    return db.query(models.Article).filter(models.Article.id == article_id).first()


def get_articles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Article).offset(skip).limit(limit).all()


def create_article(db: Session, article: schemas.ArticleCreate):
    db_article = models.Article(**article.model_dump())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


def update_article(db: Session, article: schemas.ArticleUpdate, article_id: int):
    db_article = get_article(db, article_id)
    if db_article:
        update_data = article.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_article, key, value)
        db.commit()
        db.refresh(db_article)
    return db_article


def delete_article(db: Session, article_id: int):
    db_article = get_article(db, article_id)
    if db_article:
        db.delete(db_article)
        db.commit()
    return db_article


def get_article_by_title(db: Session, title: str):
    return db.query(models.Article).filter(models.Article.title == title).first()


def search_articles(db: Session, keyword: str, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Article)
        .filter(
            models.Article.title.contains(keyword)
            | models.Article.content.contains(keyword)
        )
        .offset(skip)
        .limit(limit)
        .all()
    )
