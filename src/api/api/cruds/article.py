from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import api.models as models
import api.schemas as schemas
from api.setup_logger import setup_logger

logger, log_decorator = setup_logger(__name__)


async def get_article(db: AsyncSession, article_id: int):
    logger.info(f"Fetching article with ID: {article_id}")
    try:
        result = await db.execute(
            select(models.Article).filter(models.Article.id == article_id)
        )
        article = result.scalars().first()
        if article:
            logger.info(f"Article with ID: {article_id} fetched successfully")
        else:
            logger.warning(f"Article with ID: {article_id} not found")
        return article
    except Exception as e:
        logger.error(f"Failed to fetch article with ID: {article_id}. Error: {e}")
        raise


async def get_articles(db: AsyncSession, skip: int = 0, limit: int = 100):
    logger.info("Fetching articles")
    try:
        result = await db.execute(select(models.Article).offset(skip).limit(limit))
        articles = result.scalars().all()
        logger.info("Articles fetched successfully")
        return articles
    except Exception as e:
        logger.error(f"Failed to fetch articles. Error: {e}")
        raise


async def create_article(db: AsyncSession, article: schemas.ArticleCreate):
    logger.info("Creating new article")
    try:
        db_article = models.Article(
            **article.model_dump(),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        db.add(db_article)
        await db.commit()
        await db.refresh(db_article)
        logger.info("New article created successfully")
        return db_article
    except Exception as e:
        logger.error(f"Failed to create new article. Error: {e}")
        raise


async def update_article(
    db: AsyncSession, article: schemas.ArticleUpdate, article_id: int
):
    logger.info(f"Updating article with ID: {article_id}")
    try:
        result = await db.execute(
            select(models.Article).filter(models.Article.id == article_id)
        )
        db_article = result.scalars().first()
        if db_article:
            update_data = {
                **article.model_dump(exclude_unset=True),
                "updated_at": datetime.now(),
            }
            for key, value in update_data.items():
                setattr(db_article, key, value)
            await db.commit()
            await db.refresh(db_article)
            logger.info(f"Article with ID: {article_id} updated successfully")
            return db_article
        else:
            logger.warning(f"Article with ID: {article_id} not found")
            return None
    except Exception as e:
        logger.error(f"Failed to update article with ID: {article_id}. Error: {e}")
        raise


async def delete_article(db: AsyncSession, article_id: int) -> bool:
    logger.info(f"Deleting article with ID: {article_id}")
    try:
        result = await db.execute(
            select(models.Article).filter(models.Article.id == article_id)
        )
        db_article = result.scalars().first()
        if db_article:
            await db.delete(db_article)
            await db.commit()
            logger.info(f"Article with ID: {article_id} deleted successfully")
            return True
        else:
            logger.warning(f"Article with ID: {article_id} not found")
            return False
    except Exception as e:
        logger.error(f"Failed to delete article with ID: {article_id}. Error: {e}")
        raise


async def get_article_by_title(db: AsyncSession, title: str):
    logger.info(f"Fetching article with title: {title}")
    try:
        result = await db.execute(
            select(models.Article).filter(models.Article.title == title)
        )
        article = result.scalars().first()
        if article:
            logger.info(f"Article with title: {title} fetched successfully")
        else:
            logger.warning(f"Article with title: {title} not found")
        return article
    except Exception as e:
        logger.error(f"Failed to fetch article with title: {title}. Error: {e}")
        raise


async def search_articles(
    db: AsyncSession, keyword: str, skip: int = 0, limit: int = 100
):
    logger.info(f"Searching articles with keyword: {keyword}")
    try:
        result = await db.execute(
            select(models.Article)
            .filter(
                models.Article.title.contains(keyword)
                | models.Article.content.contains(keyword)
            )
            .offset(skip)
            .limit(limit)
        )
        articles = result.scalars().all()
        logger.info(f"Articles with keyword: {keyword} fetched successfully")
        return articles
    except Exception as e:
        logger.error(f"Failed to search articles with keyword: {keyword}. Error: {e}")
        raise
