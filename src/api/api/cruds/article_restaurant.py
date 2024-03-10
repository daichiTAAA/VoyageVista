from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import api.models as models
import api.schemas as schemas
from api.setup_logger import setup_logger

logger, log_decorator = setup_logger(__name__)


# 関連する記事を取得
async def get_assosicated_articles(db: AsyncSession, restaurant_id: int):
    logger.info(f"Fetching associated articles for restaurant ID: {restaurant_id}")
    try:
        result = await db.execute(
            select(models.ArticleRestaurant).filter(
                models.ArticleRestaurant.restaurant_id == restaurant_id
            )
        )
        articles = result.scalars().all()
        logger.info(
            f"Successfully fetched {len(articles)} associated articles for restaurant ID: {restaurant_id}"
        )
        return articles
    except Exception as e:
        logger.error(
            f"Failed to fetch associated articles for restaurant ID: {restaurant_id}. Error: {e}"
        )
        raise


# 記事をレストランにリンク
async def link_article_to_restaurant(
    db: AsyncSession, restaurant_id: int, article_id: int
):
    logger.info(f"Linking article ID: {article_id} to restaurant ID: {restaurant_id}")
    try:
        association = models.ArticleRestaurant(
            article_id=article_id,
            restaurant_id=restaurant_id,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        db.add(association)
        await db.commit()
        logger.info(
            f"Article ID: {article_id} successfully linked to restaurant ID: {restaurant_id}"
        )
        return association
    except Exception as e:
        logger.error(
            f"Failed to link article ID: {article_id} to restaurant ID: {restaurant_id}. Error: {e}"
        )
        raise


# 記事のリンクをレストランから解除
async def unlink_article_from_restaurant(
    db: AsyncSession, restaurant_id: int, article_id: int
):
    logger.info(
        f"Unlinking article ID: {article_id} from restaurant ID: {restaurant_id}"
    )
    try:
        result = await db.execute(
            select(models.ArticleRestaurant).filter(
                models.ArticleRestaurant.article_id == article_id,
                models.ArticleRestaurant.restaurant_id == restaurant_id,
            )
        )
        association = result.scalars().first()
        if association:
            await db.delete(association)
            await db.commit()
            logger.info(
                f"Article ID: {article_id} successfully unlinked from restaurant ID: {restaurant_id}"
            )
            return True
        else:
            logger.warning(
                f"No association found for article ID: {article_id} with restaurant ID: {restaurant_id}"
            )
            return False
    except Exception as e:
        logger.error(
            f"Failed to unlink article ID: {article_id} from restaurant ID: {restaurant_id}. Error: {e}"
        )
        raise


# 記事とレストランの関連付けを更新
async def update_article_restaurant_association(
    db: AsyncSession, restaurant_id: int, article_id: int
):
    logger.info(
        f"Updating association for article ID: {article_id} and restaurant ID: {restaurant_id}"
    )
    try:
        result = await db.execute(
            select(models.ArticleRestaurant).filter(
                models.ArticleRestaurant.article_id == article_id,
                models.ArticleRestaurant.restaurant_id == restaurant_id,
            )
        )
        association = result.scalars().first()
        if association:
            association.updated_at = datetime.now()
            await db.commit()
            logger.info(
                f"Association for article ID: {article_id} and restaurant ID: {restaurant_id} updated"
            )
            return association
        else:
            logger.warning(
                f"No association found to update for article ID: {article_id} with restaurant ID: {restaurant_id}"
            )
            return None
    except Exception as e:
        logger.error(
            f"Failed to update association for article ID: {article_id} and restaurant ID: {restaurant_id}. Error: {e}"
        )
        raise
