from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models, schemas


async def get_cultural_insight(db: AsyncSession, cultural_insight_id: int):
    result = await db.execute(
        select(models.CulturalInsight).filter(
            models.CulturalInsight.id == cultural_insight_id
        )
    )
    return result.scalars().first()


async def get_cultural_insights(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.CulturalInsight).offset(skip).limit(limit))
    return result.scalars().all()


async def create_cultural_insight(
    db: AsyncSession, cultural_insight: schemas.CulturalInsightCreate, article_id: int
):
    db_cultural_insight = models.CulturalInsight(
        **cultural_insight.model_dump(), article_id=article_id
    )
    db.add(db_cultural_insight)
    await db.commit()
    await db.refresh(db_cultural_insight)
    return db_cultural_insight


async def update_cultural_insight(
    db: AsyncSession,
    cultural_insight: schemas.CulturalInsightUpdate,
    cultural_insight_id: int,
):
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
    return db_cultural_insight


async def delete_cultural_insight(db: AsyncSession, cultural_insight_id: int):
    result = await db.execute(
        select(models.CulturalInsight).filter(
            models.CulturalInsight.id == cultural_insight_id
        )
    )
    db_cultural_insight = result.scalars().first()
    if db_cultural_insight:
        await db.delete(db_cultural_insight)
        await db.commit()


async def get_cultural_insights_by_article(
    db: AsyncSession, article_id: int, skip: int = 0, limit: int = 100
):
    result = await db.execute(
        select(models.CulturalInsight)
        .filter(models.CulturalInsight.article_id == article_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()
