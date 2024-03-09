from datetime import datetime

from sqlalchemy.orm import Session

import models, schemas


def get_assosicated_articles(db: Session, restaurant_id: int):
    return (
        db.query(models.ArticleRestaurant)
        .filter(models.ArticleRestaurant.restaurant_id == restaurant_id)
        .all()
    )


def link_article_to_restaurant(db: Session, restaurant_id: int, article_id: int):
    association = models.ArticleRestaurant(
        article_id=article_id, restaurant_id=restaurant_id
    )
    db.add(association)
    db.commit()
    return association


def unlink_article_from_restaurant(db: Session, restaurant_id: int, article_id: int):
    association = (
        db.query(models.ArticleRestaurant)
        .filter(
            models.ArticleRestaurant.article_id == article_id,
            models.ArticleRestaurant.restaurant_id == restaurant_id,
        )
        .first()
    )
    if association:
        db.delete(association)
        db.commit()
        return True
    return False


def update_article_restaurant_association(
    db: Session, restaurant_id: int, article_id: int
):
    association = (
        db.query(models.ArticleRestaurant)
        .filter(
            models.ArticleRestaurant.article_id == article_id,
            models.ArticleRestaurant.restaurant_id == restaurant_id,
        )
        .first()
    )
    if association:
        association.updated_at = datetime.now()
        db.commit()
        return association
    return None
