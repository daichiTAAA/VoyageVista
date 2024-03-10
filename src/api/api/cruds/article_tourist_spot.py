from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import api.models as models
from api.setup_logger import setup_logger

logger, log_decorator = setup_logger(__name__)


async def get_assosicated_articles(db: AsyncSession, tourist_spot_id: int):
    logger.info(f"Fetching associated articles for tourist spot ID: {tourist_spot_id}")
    try:
        result = await db.execute(
            select(models.ArticleTouristSpot).filter(
                models.ArticleTouristSpot.tourist_spot_id == tourist_spot_id
            )
        )
        articles = result.scalars().all()
        logger.info(
            f"Successfully fetched associated articles for tourist spot ID: {tourist_spot_id}"
        )
        return articles
    except Exception as e:
        logger.error(
            f"Error fetching associated articles for tourist spot ID: {tourist_spot_id}. Error: {e}"
        )
        raise


async def link_article_to_tourist_spot(
    db: AsyncSession, tourist_spot_id: int, article_id: int
):
    logger.info(
        f"Linking article ID: {article_id} to tourist spot ID: {tourist_spot_id}"
    )
    try:
        association = models.ArticleTouristSpot(
            article_id=article_id,
            tourist_spot_id=tourist_spot_id,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        db.add(association)
        await db.commit()
        await db.refresh(association)
        logger.info(
            f"Successfully linked article ID: {article_id} to tourist spot ID: {tourist_spot_id}"
        )
        return association
    except Exception as e:
        logger.error(
            f"Error linking article ID: {article_id} to tourist spot ID: {tourist_spot_id}. Error: {e}"
        )
        raise


async def unlink_article_from_tourist_spot(
    db: AsyncSession, tourist_spot_id: int, article_id: int
):
    logger.info(
        f"Unlinking article ID: {article_id} from tourist spot ID: {tourist_spot_id}"
    )
    try:
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
            logger.info(
                f"Successfully unlinked article ID: {article_id} from tourist spot ID: {tourist_spot_id}"
            )
            return True
        else:
            logger.warning(
                f"No association found to unlink article ID: {article_id} from tourist spot ID: {tourist_spot_id}"
            )
            return False
    except Exception as e:
        logger.error(
            f"Error unlinking article ID: {article_id} from tourist spot ID: {tourist_spot_id}. Error: {e}"
        )
        raise


async def update_article_tourist_spot_association(
    db: AsyncSession, tourist_spot_id: int, article_id: int
):
    logger.info(
        f"Updating association for article ID: {article_id} and tourist spot ID: {tourist_spot_id}"
    )
    try:
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
            logger.info(
                f"Successfully updated association for article ID: {article_id} and tourist spot ID: {tourist_spot_id}"
            )
            return association
        else:
            logger.warning(
                f"No association found to update for article ID: {article_id} and tourist spot ID: {tourist_spot_id}"
            )
            return None
    except Exception as e:
        logger.error(
            f"Error updating association for article ID: {article_id} and tourist spot ID: {tourist_spot_id}. Error: {e}"
        )
        raise
