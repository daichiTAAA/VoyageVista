from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models


async def get_assosicated_articles(db: AsyncSession, tourist_spot_id: int):
    result = await db.execute(
        select(models.ArticleTouristSpot).filter(
            models.ArticleTouristSpot.tourist_spot_id == tourist_spot_id
        )
    )
    return result.scalars().all()


async def link_article_to_tourist_spot(
    db: AsyncSession, tourist_spot_id: int, article_id: int
):
    association = models.ArticleTouristSpot(
        article_id=article_id, tourist_spot_id=tourist_spot_id
    )
    db.add(association)
    await db.commit()
    await db.refresh(association)
    return association


async def unlink_article_from_tourist_spot(
    db: AsyncSession, tourist_spot_id: int, article_id: int
):
    result = await db.execute(
        select(models.ArticleTouristSpot).filter(
            models.ArticleTouristSpot.article_id == article_id,
            models.ArticleTouristSpot.tourist_spot_id == tourist_spot_id,
        )
    )
    association = result.scalars().first()
    if association:
        await db.delete(association)
        await db.commit()
        return True
    return False


async def update_article_tourist_spot_association(
    db: AsyncSession, tourist_spot_id: int, article_id: int
):
    result = await db.execute(
        select(models.ArticleTouristSpot).filter(
            models.ArticleTouristSpot.article_id == article_id,
            models.ArticleTouristSpot.tourist_spot_id == tourist_spot_id,
        )
    )
    association = result.scalars().first()
    if association:
        association.updated_at = datetime.now()
        await db.commit()
        return association
    return None
