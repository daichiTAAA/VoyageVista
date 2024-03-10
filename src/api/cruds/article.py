from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models, schemas


async def get_article(db: AsyncSession, article_id: int):
    result = await db.execute(
        select(models.Article).filter(models.Article.id == article_id)
    )
    return result.scalars().first()


async def get_articles(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Article).offset(skip).limit(limit))
    return result.scalars().all()


async def create_article(db: AsyncSession, article: schemas.ArticleCreate):
    db_article = models.Article(**article.model_dump())
    db.add(db_article)
    await db.commit()
    await db.refresh(db_article)
    return db_article


async def update_article(
    db: AsyncSession, article: schemas.ArticleUpdate, article_id: int
):
    result = await db.execute(
        select(models.Article).filter(models.Article.id == article_id)
    )
    db_article = result.scalars().first()
    if db_article:
        update_data = article.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_article, key, value)
        await db.commit()
        await db.refresh(db_article)
    return db_article


async def delete_article(db: AsyncSession, article_id: int):
    result = await db.execute(
        select(models.Article).filter(models.Article.id == article_id)
    )
    db_article = result.scalars().first()
    if db_article:
        await db.delete(db_article)
        await db.commit()


async def get_article_by_title(db: AsyncSession, title: str):
    result = await db.execute(
        select(models.Article).filter(models.Article.title == title)
    )
    return result.scalars().first()


async def search_articles(
    db: AsyncSession, keyword: str, skip: int = 0, limit: int = 100
):
    result = await db.execute(
        select(models.Article)
        .filter(
            models.Article.title.contains(keyword)
            | models.Article.content.contains(keyword)
        )
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()
