from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models, schemas
from setup_logger import setup_logger

logger, log_decorator = setup_logger(__name__)


async def get_cultural_insight(db: AsyncSession, cultural_insight_id: int):
    logger.info(f"Attempting to fetch cultural insight with ID: {cultural_insight_id}")
    try:
        result = await db.execute(
            select(models.CulturalInsight).filter(
                models.CulturalInsight.id == cultural_insight_id
            )
        )
        cultural_insight = result.scalars().first()
        if cultural_insight:
            logger.info(
                f"Successfully fetched cultural insight with ID: {cultural_insight_id}"
            )
        else:
            logger.warning(f"Cultural insight with ID: {cultural_insight_id} not found")
        return cultural_insight
    except Exception as e:
        logger.error(
            f"Error fetching cultural insight with ID: {cultural_insight_id} - {e}"
        )
        raise


async def get_cultural_insights(db: AsyncSession, skip: int = 0, limit: int = 100):
    logger.info("Fetching cultural insights")
    try:
        result = await db.execute(
            select(models.CulturalInsight).offset(skip).limit(limit)
        )
        cultural_insights = result.scalars().all()
        logger.info("Successfully fetched cultural insights")
        return cultural_insights
    except Exception as e:
        logger.error(f"Error fetching cultural insights - {e}")
        raise


async def create_cultural_insight(
    db: AsyncSession, cultural_insight: schemas.CulturalInsightCreate, article_id: int
):
    logger.info(f"Creating a new cultural insight for article ID: {article_id}")
    try:
        db_cultural_insight = models.CulturalInsight(
            **cultural_insight.model_dump(), article_id=article_id
        )
        db.add(db_cultural_insight)
        await db.commit()
        await db.refresh(db_cultural_insight)
        logger.info("Successfully created a new cultural insight")
        return db_cultural_insight
    except Exception as e:
        logger.error("Error creating a new cultural insight - {e}")
        raise


async def update_cultural_insight(
    db: AsyncSession,
    cultural_insight: schemas.CulturalInsightUpdate,
    cultural_insight_id: int,
):
    logger.info(f"Updating cultural insight with ID: {cultural_insight_id}")
    try:
        result = await db.execute(
            select(models.CulturalInsight).filter(
                models.CulturalInsight.id == cultural_insight_id
            )
        )
        db_cultural_insight = result.scalars().first()
        if db_cultural_insight:
            update_data = cultural_insight.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_cultural_insight, key, value)
            await db.commit()
            await db.refresh(db_cultural_insight)
            logger.info("Successfully updated cultural insight")
        else:
            logger.warning(f"Cultural insight with ID: {cultural_insight_id} not found")
        return db_cultural_insight
    except Exception as e:
        logger.error(
            f"Error updating cultural insight with ID: {cultural_insight_id} - {e}"
        )
        raise


async def delete_cultural_insight(db: AsyncSession, cultural_insight_id: int):
    logger.info(f"Deleting cultural insight with ID: {cultural_insight_id}")
    try:
        result = await db.execute(
            select(models.CulturalInsight).filter(
                models.CulturalInsight.id == cultural_insight_id
            )
        )
        db_cultural_insight = result.scalars().first()
        if db_cultural_insight:
            await db.delete(db_cultural_insight)
            await db.commit()
            logger.info("Successfully deleted cultural insight")
        else:
            logger.warning(f"Cultural insight with ID: {cultural_insight_id} not found")
    except Exception as e:
        logger.error(
            f"Error deleting cultural insight with ID: {cultural_insight_id} - {e}"
        )
        raise


async def get_cultural_insights_by_article(
    db: AsyncSession, article_id: int, skip: int = 0, limit: int = 100
):
    logger.info(f"Fetching cultural insights for article ID: {article_id}")
    try:
        result = await db.execute(
            select(models.CulturalInsight)
            .filter(models.CulturalInsight.article_id == article_id)
            .offset(skip)
            .limit(limit)
        )
        cultural_insights = result.scalars().all()
        logger.info(
            f"Successfully fetched cultural insights for article ID: {article_id}"
        )
        return cultural_insights
    except Exception as e:
        logger.error(
            f"Error fetching cultural insights for article ID: {article_id} - {e}"
        )
        raise
