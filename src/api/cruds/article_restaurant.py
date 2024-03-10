from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models, schemas


# 関連する記事を取得
async def get_assosicated_articles(db: AsyncSession, restaurant_id: int):
    result = await db.execute(
        select(models.ArticleRestaurant).filter(
            models.ArticleRestaurant.restaurant_id == restaurant_id
        )
    )
    return result.scalars().all()


# 記事をレストランにリンク
async def link_article_to_restaurant(
    db: AsyncSession, restaurant_id: int, article_id: int
):
    association = models.ArticleRestaurant(
        article_id=article_id, restaurant_id=restaurant_id
    )
    db.add(association)
    await db.commit()
    return association


# 記事のリンクをレストランから解除
async def unlink_article_from_restaurant(
    db: AsyncSession, restaurant_id: int, article_id: int
):
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
        return True
    return False


# 記事とレストランの関連付けを更新
async def update_article_restaurant_association(
    db: AsyncSession, restaurant_id: int, article_id: int
):
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
        return association
    return None
